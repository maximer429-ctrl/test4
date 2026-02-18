/**
 * Animation - Handles frame-based sprite animation
 */
export class Animation {
    constructor(frames, fps = 10, loop = true) {
        this.frames = frames; // Array of frame objects with { x, y, width, height }
        this.fps = fps;
        this.loop = loop;
        this.currentFrame = 0;
        this.frameTime = 1000 / fps; // milliseconds per frame
        this.elapsedTime = 0;
        this.playing = false;
        this.finished = false;
    }

    /**
     * Update animation state
     * @param {number} deltaTime - Time elapsed since last update in milliseconds
     */
    update(deltaTime) {
        if (!this.playing || this.finished) {
            return;
        }

        this.elapsedTime += deltaTime;

        if (this.elapsedTime >= this.frameTime) {
            this.elapsedTime -= this.frameTime;
            this.currentFrame++;

            if (this.currentFrame >= this.frames.length) {
                if (this.loop) {
                    this.currentFrame = 0;
                } else {
                    this.currentFrame = this.frames.length - 1;
                    this.finished = true;
                    this.playing = false;
                }
            }
        }
    }

    /**
     * Get current frame data
     * @returns {Object} Current frame object
     */
    getCurrentFrame() {
        return this.frames[this.currentFrame];
    }

    /**
     * Start playing animation
     */
    play() {
        this.playing = true;
        this.finished = false;
    }

    /**
     * Pause animation
     */
    pause() {
        this.playing = false;
    }

    /**
     * Reset animation to first frame
     */
    reset() {
        this.currentFrame = 0;
        this.elapsedTime = 0;
        this.finished = false;
    }

    /**
     * Stop and reset animation
     */
    stop() {
        this.pause();
        this.reset();
    }

    /**
     * Clone animation for instancing
     * @returns {Animation} New animation instance
     */
    clone() {
        const anim = new Animation([...this.frames], this.fps, this.loop);
        return anim;
    }
}
