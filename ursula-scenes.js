const { ursulaPatterns, getPhraseSsml } = require('./ursula-phrases');
const { getSlangSsml, getSlangExample, slangTerms } = require('./ursula-slang');

// Scene 1: Gossip at the Salon
function salonGossipScene() {
    return `<speak>
        ${getPhraseSsml('greetings', 'generalOpener')}
        ${getPhraseSsml('transitions', 'sharingSecret')}
        That ${getSlangSsml('biddy')} from ${getSlangSsml('upTheCorner')} is ${getSlangSsml('wicked')} upset.
        ${getPhraseSsml('transitions', 'addingDetail')}
        She got ${getSlangSsml('bagged')} at the ${getSlangSsml('packie')}.
        ${getPhraseSsml('closings', 'standard')}
    </speak>`;
}

// Scene 2: Giving Directions
function directionsScene() {
    return `<speak>
        ${getPhraseSsml('greetings', 'casualUpdate')}
        Listen honey, it's ${getSlangSsml('wicked')} easy.
        ${getSlangSsml('bangAUey')} at the ${getSlangSsml('rotary')},
        go past the ${getSlangSsml('bubbler')},
        and it's right ${getSlangSsml('upTheCorner')}.
        Can't miss it, ${getSlangSsml('sugar')}.
        ${getPhraseSsml('closings', 'quickUpdate')}
    </speak>`;
}

// Scene 3: Weather Warning
function weatherScene() {
    return `<speak>
        ${getPhraseSsml('greetings', 'bigNews')}
        We're getting a ${getSlangSsml('wicked')} bad ${getSlangSsml('norEaster')}.
        Better head to the ${getSlangSsml('packie')} before the ${getSlangSsml('flurries')} start.
        ${getPhraseSsml('closings', 'lightHearted')}
    </speak>`;
}

// Scene 4: Restaurant Recommendation
function foodScene() {
    return `<speak>
        ${getPhraseSsml('greetings', 'casualUpdate')}
        You gotta try this new spot, ${getSlangSsml('kid')}.
        They got the best ${getSlangSsml('grinder')} and ${getSlangSsml('frappe')}.
        ${getSlangSsml('wicked')} good ${getSlangSsml('chowdah')}.
        ${getPhraseSsml('closings', 'standard')}
    </speak>`;
}

// Scene 5: Giving Advice
function adviceScene() {
    return `<speak>
        ${getPhraseSsml('greetings', 'bigNews')}
        ${getPhraseSsml('transitions', 'beforeCriticism')}
        Don't be such a ${getSlangSsml('chucklehead')}.
        That ${getSlangSsml('tool')} is ${getSlangSsml('wicked')} bad news.
        ${getPhraseSsml('encouragement', 'support')}
        ${getPhraseSsml('closings', 'afterToughNews')}
    </speak>`;
}

// Scene 6: Sports Talk
function sportsScene() {
    return `<speak>
        ${getPhraseSsml('greetings', 'excited')}
        The Sox were ${getSlangSsml('wicked')} ${getSlangSsml('pissa')} last night!
        That ${getSlangSsml('hardo')} from New York tried talking smack,
        but I told him "So don't I!"
        ${getPhraseSsml('closings', 'lightHearted')}
    </speak>`;
}

// Scene 7: Coffee Shop Order
function coffeeScene() {
    return `<speak>
        ${getPhraseSsml('greetings', 'casualUpdate')}
        Lemme get a ${getSlangSsml('regular')} and a ${getSlangSsml('cruller')}.
        And throw in some of them ${getSlangSsml('jimmies')} on top.
        ${getSlangSsml('wicked')} sweet of ya, ${getSlangSsml('kid')}.
        ${getPhraseSsml('closings', 'quickUpdate')}
    </speak>`;
}

// Export all scenes
module.exports = {
    salonGossipScene,
    directionsScene,
    weatherScene,
    foodScene,
    adviceScene,
    sportsScene,
    coffeeScene
}; 