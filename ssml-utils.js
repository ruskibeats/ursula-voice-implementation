const patterns = require('./ssml-patterns');

class SSMLUtils {
    static applyPattern(type, name, text, options = {}) {
        const category = patterns[type];
        if (!category || !category[name]) {
            throw new Error(`Pattern not found: ${type}.${name}`);
        }

        let pattern = category[name].pattern;
        
        // Replace text placeholder
        pattern = pattern.replace('$TEXT', text);
        
        // Replace any additional placeholders from options
        Object.keys(options).forEach(key => {
            pattern = pattern.replace(`$${key.toUpperCase()}`, options[key]);
        });

        return pattern;
    }

    static wrapInSpeak(ssml) {
        return `<speak>${ssml}</speak>`;
    }

    static combinePatterns(patterns) {
        return patterns.join('');
    }

    static validateSSML(ssml) {
        // Basic validation - check for matching tags
        const openTags = ssml.match(/<[^/][^>]*>/g) || [];
        const closeTags = ssml.match(/<\/[^>]+>/g) || [];
        
        if (openTags.length !== closeTags.length) {
            throw new Error('Mismatched SSML tags');
        }

        return true;
    }
}

module.exports = SSMLUtils; 