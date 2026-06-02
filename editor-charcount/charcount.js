module.exports = {
    counter: function(t) {
        // Check for undefined or null
        if (t === undefined || t === null) {
            throw new TypeError("Input cannot be null or undefined");
        }

        // Ensure input is a string
        const text = String(t);

        // Check for empty string after trimming
        if (text.trim() === '') {
            throw new TypeError("Input cannot be empty");
        }

        // Remove all whitespace characters and count remaining characters
        return text.replace(/\s/g, '').length;
    },

    validate: function(t) {
        try {
            this.counter(t);
            return {
                valid: true,
                message: "Valid input"
            };
        } catch (error) {
            return {
                valid: false,
                message: error.message
            };
        }
    }
};