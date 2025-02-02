#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// Import our Ursula modules
const { ursulaPatterns, getPhraseSsml } = require('./ursula-phrases');
const { getSlangSsml, getSlangExample, slangTerms } = require('./ursula-slang');
const scenes = require('./ursula-scenes');

// Function to save SSML to file
function saveSsml(ssml, filename) {
    const outputPath = path.join(__dirname, 'output', filename);
    fs.mkdirSync(path.join(__dirname, 'output'), { recursive: true });
    fs.writeFileSync(outputPath, ssml);
    console.log(`Saved SSML to ${outputPath}`);
}

// Generate all scenes
console.log('Generating scenes...\n');

// Salon Gossip
saveSsml(scenes.salonGossipScene(), 'scene_salon_gossip.ssml');

// Giving Directions
saveSsml(scenes.directionsScene(), 'scene_directions.ssml');

// Weather Warning
saveSsml(scenes.weatherScene(), 'scene_weather.ssml');

// Restaurant Recommendation
saveSsml(scenes.foodScene(), 'scene_food.ssml');

// Giving Advice
saveSsml(scenes.adviceScene(), 'scene_advice.ssml');

// Sports Talk
saveSsml(scenes.sportsScene(), 'scene_sports.ssml');

// Coffee Shop Order
saveSsml(scenes.coffeeScene(), 'scene_coffee.ssml');

console.log('\nAll scenes generated. Check the output directory for the SSML files.');

// How to use:
console.log('\nTo use these files with Amazon Polly:');
console.log('1. Choose a scene file from the output directory');
console.log('2. Run the following command (replace SCENE_NAME):');
console.log('   aws polly synthesize-speech \\');
console.log('     --text-type ssml \\');
console.log('     --output-format mp3 \\');
console.log('     --voice-id Ruth \\');
console.log('     --text file://output/scene_SCENE_NAME.ssml \\');
console.log('     output/scene_SCENE_NAME.mp3');

console.log('\nExample for the salon gossip scene:');
console.log('   aws polly synthesize-speech \\');
console.log('     --text-type ssml \\');
console.log('     --output-format mp3 \\');
console.log('     --voice-id Ruth \\');
console.log('     --text file://output/scene_salon_gossip.ssml \\');
console.log('     output/scene_salon_gossip.mp3'); 