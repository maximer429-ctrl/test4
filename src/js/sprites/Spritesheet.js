/**
 * Spritesheet - Handles loading and extracting frames from sprite sheet images
 */
export class Spritesheet {
    constructor(imagePath, frameWidth, frameHeight) {
        this.imagePath = imagePath;
        this.frameWidth = frameWidth;
        this.frameHeight = frameHeight;
        this.image = null;
        this.loaded = false;
        this.loadPromise = null;
    }

    /**
     * Load the spritesheet image
     * @returns {Promise} Resolves when image is loaded
     */
    load() {
        if (this.loadPromise) {
            return this.loadPromise;
        }

        this.loadPromise = new Promise((resolve, reject) => {
            this.image = new Image();
            
            this.image.onload = () => {
                this.loaded = true;
                this.columns = Math.floor(this.image.width / this.frameWidth);
                this.rows = Math.floor(this.image.height / this.frameHeight);
                resolve(this);
            };

            this.image.onerror = () => {
                reject(new Error(`Failed to load spritesheet: ${this.imagePath}`));
            };

            this.image.src = this.imagePath;
        });

        return this.loadPromise;
    }

    /**
     * Get frame coordinates from frame index and row
     * @param {number} frameIndex - Frame column index
     * @param {number} row - Row index (default 0)
     * @returns {Object} Frame data { x, y, width, height }
     */
    getFrame(frameIndex, row = 0) {
        return {
            x: frameIndex * this.frameWidth,
            y: row * this.frameHeight,
            width: this.frameWidth,
            height: this.frameHeight
        };
    }

    /**
     * Get array of frames for animation
     * @param {Array<number>} frameIndices - Array of frame column indices
     * @param {number} row - Row index
     * @returns {Array<Object>} Array of frame data objects
     */
    getFrames(frameIndices, row = 0) {
        return frameIndices.map(index => this.getFrame(index, row));
    }

    /**
     * Draw a specific frame to a canvas context
     * @param {CanvasRenderingContext2D} ctx - Canvas 2D context
     * @param {number} frameIndex - Frame column index
     * @param {number} row - Row index
     * @param {number} x - Destination X coordinate
     * @param {number} y - Destination Y coordinate
     * @param {number} width - Destination width (optional, defaults to frameWidth)
     * @param {number} height - Destination height (optional, defaults to frameHeight)
     */
    drawFrame(ctx, frameIndex, row, x, y, width = null, height = null) {
        if (!this.loaded) {
            console.warn('Spritesheet not loaded yet');
            return;
        }

        const frame = this.getFrame(frameIndex, row);
        const dstWidth = width || this.frameWidth;
        const dstHeight = height || this.frameHeight;

        ctx.drawImage(
            this.image,
            frame.x, frame.y, frame.width, frame.height,
            x, y, dstWidth, dstHeight
        );
    }

    /**
     * Get frame data for WebGL texture rendering
     * @param {number} frameIndex - Frame column index
     * @param {number} row - Row index
     * @returns {Object} UV coordinates and dimensions for WebGL
     */
    getFrameUVs(frameIndex, row = 0) {
        if (!this.loaded) {
            return null;
        }

        const frame = this.getFrame(frameIndex, row);
        const u = frame.x / this.image.width;
        const v = frame.y / this.image.height;
        const uWidth = frame.width / this.image.width;
        const vHeight = frame.height / this.image.height;

        return {
            u: u,
            v: v,
            uWidth: uWidth,
            vHeight: vHeight,
            // Also return pixel coordinates for reference
            x: frame.x,
            y: frame.y,
            width: frame.width,
            height: frame.height
        };
    }

    /**
     * Get spritesheet metadata
     * @returns {Object} Spritesheet information
     */
    getInfo() {
        return {
            path: this.imagePath,
            loaded: this.loaded,
            frameWidth: this.frameWidth,
            frameHeight: this.frameHeight,
            columns: this.columns || 0,
            rows: this.rows || 0,
            imageWidth: this.image ? this.image.width : 0,
            imageHeight: this.image ? this.image.height : 0
        };
    }
}
