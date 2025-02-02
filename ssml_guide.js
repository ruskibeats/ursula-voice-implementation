function SSML_Guide($input) {
    return {
        // Core SSML Patterns
        patterns: {
            emotions: {
                happy: "<amazon:emotion name=\"happy\" intensity=\"high\">",
                excited: "<amazon:emotion name=\"excited\" intensity=\"high\">",
                disappointed: "<amazon:emotion name=\"disappointed\" intensity=\"medium\">",
                serious: "<amazon:emotion name=\"serious\" intensity=\"medium\">"
            },
            styles: {
                excited: "<prosody rate=\"fast\" pitch=\"+2st\">",
                dramatic: "<prosody rate=\"slow\" pitch=\"-2st\">",
                loud: "<prosody volume=\"loud\">",
                soft: "<prosody volume=\"soft\">",
                whispered: "<amazon:effect name=\"whispered\">",
                emphasis: "<emphasis level=\"strong\">"
            },
            breaks: {
                standard: "<break time=\"300ms\"/>",
                quick: "<break time=\"200ms\"/>",
                transition: "<break time=\"400ms\"/>"
            }
        },

        // Message Templates
        templates: {
            taskPriority: [
                "<prosody volume=\"loud\">LISTEN UP!</prosody><break time=\"200ms\"/>",
                "<emphasis level=\"strong\">This is critical, sugar!</emphasis><break time=\"300ms\"/>",
                "<amazon:emotion name=\"serious\" intensity=\"medium\">We need to talk about something important.</amazon:emotion>"
            ],
            commentSpotting: [
                "<prosody rate=\"fast\" pitch=\"+2st\">Oh! What's this?</prosody><break time=\"200ms\"/>",
                "<emphasis level=\"strong\">Hold everything!</emphasis><break time=\"300ms\"/>",
                "<amazon:emotion name=\"excited\" intensity=\"high\">Sugar, you won't believe this comment!</amazon:emotion>"
            ],
            quickWins: [
                "<amazon:emotion name=\"happy\" intensity=\"high\">Now for some good news!</amazon:emotion>",
                "<prosody rate=\"fast\" pitch=\"+2st\">These are wicked easy wins!</prosody>",
                "<prosody volume=\"loud\">Check these quick ones out!</prosody>"
            ]
        }
    };
}
