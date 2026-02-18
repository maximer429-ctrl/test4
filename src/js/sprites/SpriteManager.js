import { Spritesheet } from './Spritesheet.js';
import { Animation } from './Animation.js';

/**
 * SpriteManager - Central sprite management system
 * Works with both Canvas 2D and WebGL contexts
 */
export class SpriteManager {
    constructor() {
        this.config = null;
        this.spritesheets = new Map();
        this.animations = new Map();
        this.loadedPromise = null;
    }

    /**
     * Load sprite configuration and all spritesheets
     * @param {string} configPath - Path to sprite config JSON
     * @returns {Promise} Resolves when all assets are loaded
     */
    async load(configPath = 'assets/sprites/config.json') {
        if (this.loadedPromise) {
            return this.loadedPromise;
        }

        this.loadedPromise = (async () => {
            try {
                // Load configuration
                const response = await fetch(configPath);
                if (!response.ok) {
                    throw new Error(`Failed to load sprite config: ${response.statusText}`);
                }
                this.config = await response.json();

                // Load all spritesheets
                const loadPromises = [];
                for (const [sheetName, sheetData] of Object.entries(this.config.spritesheets)) {
                    const spritesheet = new Spritesheet(
                        sheetData.path,
                        sheetData.frameWidth,
                        sheetData.frameHeight
                    );
                    this.spritesheets.set(sheetName, spritesheet);
                    loadPromises.push(spritesheet.load());

                    // Create animation templates
                    for (const [spriteName, spriteData] of Object.entries(sheetData.sprites)) {
                        const frames = spritesheet.getFrames(spriteData.frames, spriteData.row);
                        const animation = new Animation(frames, spriteData.fps, spriteData.loop);
                        this.animations.set(spriteName, animation);
                    }
                }

                await Promise.all(loadPromises);
                console.log(`✓ Loaded ${this.spritesheets.size} spritesheets with ${this.animations.size} animations`);
                return this;
            } catch (error) {
                console.error('Failed to load sprites:', error);
                throw error;
            }
        })();

        return this.loadedPromise;
    }

    /**
     * Get a spritesheet by name
     * @param {string} name - Spritesheet name
     * @returns {Spritesheet|null}
     */
    getSpritesheet(name) {
        return this.spritesheets.get(name) || null;
    }

    /**
     * Create a new animation instance (cloned from template)
     * @param {string} name - Animation name
     * @returns {Animation|null}
     */
    createAnimation(name) {
        const template = this.animations.get(name);
        return template ? template.clone() : null;
    }

    /**
     * Get animation template (don't modify!)
     * @param {string} name - Animation name
     * @returns {Animation|null}
     */
    getAnimationTemplate(name) {
        return this.animations.get(name) || null;
    }

    /**
     * Draw a sprite frame using Canvas 2D context
     * @param {CanvasRenderingContext2D} ctx - Canvas 2D context
     * @param {string} spriteName - Sprite/animation name
     * @param {number} frameIndex - Frame index (default 0)
     * @param {number} x - X position
     * @param {number} y - Y position
     * @param {number} width - Width (optional)
     * @param {number} height - Height (optional)
     */
    draw(ctx, spriteName, frameIndex = 0, x, y, width = null, height = null) {
        const anim = this.animations.get(spriteName);
        if (!anim) {
            console.warn(`Animation not found: ${spriteName}`);
            return;
        }

        const frame = anim.frames[Math.min(frameIndex, anim.frames.length - 1)];
        const spritesheet = this.findSpritesheetForSprite(spriteName);
        
        if (!spritesheet || !spritesheet.loaded) {
            console.warn(`Spritesheet not loaded for: ${spriteName}`);
            return;
        }

        const dstWidth = width || frame.width;
        const dstHeight = height || frame.height;

        ctx.drawImage(
            spritesheet.image,
            frame.x, frame.y, frame.width, frame.height,
            x, y, dstWidth, dstHeight
        );
    }

    /**
     * Draw an animation's current frame
     * @param {CanvasRenderingContext2D} ctx - Canvas 2D context
     * @param {Animation} animation - Animation instance
     * @param {number} x - X position
     * @param {number} y - Y position
     * @param {number} width - Width (optional)
     * @param {number} height - Height (optional)
     */
    drawAnimation(ctx, animation, x, y, width = null, height = null) {
        const frame = animation.getCurrentFrame();
        const spritesheet = this.findSpritesheetForFrame(frame);
        
        if (!spritesheet || !spritesheet.loaded) {
            return;
        }

        const dstWidth = width || frame.width;
        const dstHeight = height || frame.height;

        ctx.drawImage(
            spritesheet.image,
            frame.x, frame.y, frame.width, frame.height,
            x, y, dstWidth, dstHeight
        );
    }

    /**
     * Get sprite metadata
     * @param {string} spriteName - Sprite/animation name
     * @returns {Object|null} Sprite metadata
     */
    getSpriteInfo(spriteName) {
        const anim = this.animations.get(spriteName);
        if (!anim) return null;

        const spritesheet = this.findSpritesheetForSprite(spriteName);
        const sheetInfo = spritesheet ? spritesheet.getInfo() : null;

        return {
            name: spriteName,
            frameCount: anim.frames.length,
            fps: anim.fps,
            loop: anim.loop,
            frameWidth: anim.frames[0]?.width || 0,
            frameHeight: anim.frames[0]?.height || 0,
            spritesheet: sheetInfo
        };
    }

    /**
     * Get all available sprite names
     * @returns {Array<string>}
     */
    getAllSpriteNames() {
        return Array.from(this.animations.keys());
    }

    /**
     * Get sprites grouped by category (based on spritesheet)
     * @returns {Object} Sprites grouped by category
     */
    getSpritesByCategory() {
        const categories = {};
        
        for (const [sheetName, sheetData] of Object.entries(this.config.spritesheets)) {
            categories[sheetName] = Object.keys(sheetData.sprites);
        }

        return categories;
    }

    /**
     * Get ruminant metadata
     * @param {string} ruminantType - Type (cow, sheep, goat, alpaca)
     * @returns {Object|null}
     */
    getRuminantMetadata(ruminantType) {
        return this.config.metadata?.ruminants?.[ruminantType] || null;
    }

    /**
     * Get all ruminant types
     * @returns {Array<string>}
     */
    getAllRuminantTypes() {
        return Object.keys(this.config.metadata?.ruminants || {});
    }

    /**
     * Find which spritesheet contains a sprite
     * @private
     * @param {string} spriteName - Sprite name
     * @returns {Spritesheet|null}
     */
    findSpritesheetForSprite(spriteName) {
        for (const [sheetName, sheetData] of Object.entries(this.config.spritesheets)) {
            if (spriteName in sheetData.sprites) {
                return this.spritesheets.get(sheetName);
            }
        }
        return null;
    }

    /**
     * Find which spritesheet contains a frame
     * @private
     * @param {Object} frame - Frame object
     * @returns {Spritesheet|null}
     */
    findSpritesheetForFrame(frame) {
        // Try to find by matching frame dimensions
        for (const spritesheet of this.spritesheets.values()) {
            if (spritesheet.frameWidth === frame.width && 
                spritesheet.frameHeight === frame.height) {
                return spritesheet;
            }
        }
        return null;
    }

    /**
     * Check if all assets are loaded
     * @returns {boolean}
     */
    isLoaded() {
        return this.config !== null && 
               Array.from(this.spritesheets.values()).every(sheet => sheet.loaded);
    }

    /**
     * Get loading progress
     * @returns {Object} Progress info
     */
    getLoadingProgress() {
        const total = this.spritesheets.size;
        const loaded = Array.from(this.spritesheets.values()).filter(sheet => sheet.loaded).length;
        
        return {
            loaded,
            total,
            percentage: total > 0 ? (loaded / total) * 100 : 0,
            complete: loaded === total
        };
    }
}

// Create singleton instance
export const spriteManager = new SpriteManager();
