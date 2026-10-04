// =========================================================
// PIXELFORGE
// =========================================================


// =========================================================
// API
// =========================================================

const API_BASE =
    "http://127.0.0.1:5000";


// =========================================================
// ELEMENTS
// =========================================================

const promptInput =
    document.getElementById("prompt");

const negativePromptInput =
    document.getElementById("negative-prompt");

const styleSelect =
    document.getElementById("style");

const aspectRatioSelect =
    document.getElementById("aspect-ratio");

const formatSelect =
    document.getElementById("format");

const seedInput =
    document.getElementById("seed");

const randomSeedButton =
    document.getElementById("random-seed");

const generateButton =
    document.getElementById("generate-btn");

const generateText =
    document.getElementById("generate-text");

const characterCount =
    document.getElementById("character-count");

const errorMessage =
    document.getElementById("error-message");

const emptyState =
    document.getElementById("empty-state");

const loadingState =
    document.getElementById("loading-state");

const imageResult =
    document.getElementById("image-result");

const generatedImage =
    document.getElementById("generated-image");

const downloadButton =
    document.getElementById("download-btn");

const resultStatus =
    document.getElementById("result-status");

const resultPrompt =
    document.getElementById("result-prompt");

const resultStyle =
    document.getElementById("result-style");

const resultResolution =
    document.getElementById("result-resolution");

const resultFormat =
    document.getElementById("result-format");

const resultSize =
    document.getElementById("result-size");

const resultTime =
    document.getElementById("result-time");

const resultSeed =
    document.getElementById("result-seed");

const copyPromptButton =
    document.getElementById("copy-prompt-btn");

const regenerateButton =
    document.getElementById("regenerate-btn");

const historyGrid =
    document.getElementById("history-grid");

const historyEmpty =
    document.getElementById("history-empty");

const refreshHistoryButton =
    document.getElementById("refresh-history");

const clearHistoryButton =
    document.getElementById("clear-history");


// =========================================================
// PRESET PROMPTS
// =========================================================

const presets = {

    cyberpunk:
        "A futuristic cyberpunk city at night, towering neon skyscrapers, flying cars, glowing advertisements, wet streets reflecting colorful lights, cinematic atmosphere, highly detailed, dramatic lighting",

    fantasy:
        "An ancient magical kingdom surrounded by enormous mountains, a mysterious castle floating above a glowing forest, magical particles in the air, epic fantasy atmosphere, highly detailed",

    anime:
        "A beautiful anime character standing on a rooftop during sunset, detailed city skyline in the background, dramatic clouds, cinematic composition, vibrant colors, detailed anime artwork",

    cinematic:
        "A lone explorer walking through a mysterious abandoned city during heavy rain, cinematic lighting, atmospheric fog, dramatic composition, realistic details, film still",

    product:
        "A premium futuristic smartphone placed on a sleek reflective surface, professional studio lighting, dramatic shadows, luxury product photography, ultra detailed",

    architecture:
        "A futuristic architectural masterpiece in a modern city, enormous glass structures, elegant geometric design, people walking around, golden hour lighting, architectural photography",

    portrait:
        "A cinematic portrait of a mysterious young person with expressive eyes, dramatic studio lighting, shallow depth of field, detailed skin texture, professional photography",

    nature:
        "A breathtaking mountain landscape surrounded by mist, a crystal-clear lake reflecting the mountains, golden sunrise, atmospheric clouds, ultra detailed nature photography"

};


// =========================================================
// CHARACTER COUNTER
// =========================================================

promptInput.addEventListener(
    "input",
    () => {

        characterCount.textContent =
            `${promptInput.value.length} / 10000`;

    }
);


// =========================================================
// PRESET BUTTONS
// =========================================================

document.querySelectorAll(
    ".preset-btn"
).forEach(
    button => {

        button.addEventListener(
            "click",
            () => {

                const preset =
                    button.dataset.preset;


                if (
                    presets[preset]
                ) {

                    promptInput.value =
                        presets[preset];


                    characterCount.textContent =
                        `${promptInput.value.length} / 10000`;


                    promptInput.focus();

                }

            }
        );

    }
);


// =========================================================
// RANDOM SEED
// =========================================================

randomSeedButton.addEventListener(
    "click",
    () => {

        const seed =
            Math.floor(
                Math.random() *
                4294967295
            );


        seedInput.value =
            seed;

    }
);


// =========================================================
// ERROR
// =========================================================

function showError(message) {

    errorMessage.textContent =
        message;

    errorMessage.classList.remove(
        "hidden"
    );

}


function hideError() {

    errorMessage.classList.add(
        "hidden"
    );

}


// =========================================================
// LOADING
// =========================================================

function showLoading() {

    emptyState.classList.add(
        "hidden"
    );

    imageResult.classList.add(
        "hidden"
    );

    loadingState.classList.remove(
        "hidden"
    );

    resultStatus.textContent =
        "GENERATING";

    generateButton.disabled =
        true;

    generateText.textContent =
        "Generating...";

}


// =========================================================
// RESET BUTTON
// =========================================================

function resetButton() {

    generateButton.disabled =
        false;

    generateText.textContent =
        "Generate Image";

}


// =========================================================
// FORMAT FILE SIZE
// =========================================================

function formatFileSize(bytes) {

    if (!bytes) {
        return "0 B";
    }


    if (bytes < 1024) {

        return `${bytes} B`;

    }


    if (bytes < 1024 * 1024) {

        return `${(
            bytes / 1024
        ).toFixed(1)} KB`;

    }


    return `${(
        bytes /
        (1024 * 1024)
    ).toFixed(1)} MB`;

}


// =========================================================
// GENERATE IMAGE
// =========================================================

async function generateImage() {

    hideError();


    const prompt =
        promptInput.value.trim();


    const negativePrompt =
        negativePromptInput.value.trim();


    const style =
        styleSelect.value;


    const aspectRatio =
        aspectRatioSelect.value;


    const outputFormat =
        formatSelect.value;


    let seed =
        parseInt(
            seedInput.value
        );


    if (!prompt) {

        showError(
            "Please describe the image you want to generate."
        );

        promptInput.focus();

        return;

    }


    if (
        isNaN(seed) ||
        seed < 0
    ) {

        showError(
            "Please enter a valid seed."
        );

        return;

    }


    showLoading();


    try {

        const response =
            await fetch(
                `${API_BASE}/api/generate`,
                {

                    method:
                        "POST",

                    headers: {

                        "Content-Type":
                            "application/json"

                    },

                    body:
                        JSON.stringify({

                            prompt:

                                prompt,

                            negative_prompt:

                                negativePrompt,

                            aspect_ratio:

                                aspectRatio,

                            style_preset:

                                style,

                            output_format:

                                outputFormat,

                            seed:

                                seed

                        })

                }
            );


        const result =
            await response.json();


        if (
            !response.ok ||
            !result.success
        ) {

            throw new Error(
                result.error ||
                "Image generation failed."
            );

        }


        const imageUrl =
            `${API_BASE}${result.image}`;


        generatedImage.src =
            imageUrl;


        generatedImage.alt =
            result.prompt;


        downloadButton.href =
            imageUrl;


        downloadButton.download =
            result.filename;


        resultPrompt.textContent =
            result.prompt;


        resultStyle.textContent =
            result.style_preset;


        resultResolution.textContent =
            result.resolution ||
            `${result.width} × ${result.height}`;


        resultFormat.textContent =
            (
                result.output_format ||
                outputFormat
            ).toUpperCase();


        resultSize.textContent =
            formatFileSize(
                result.size
            );


        resultTime.textContent =
            `${result.generation_time || "—"} sec`;


        resultSeed.textContent =
            result.seed;


        loadingState.classList.add(
            "hidden"
        );


        emptyState.classList.add(
            "hidden"
        );


        imageResult.classList.remove(
            "hidden"
        );


        resultStatus.textContent =
            "COMPLETE";


        await loadHistory();


        imageResult.scrollIntoView({
            behavior: "smooth",
            block: "center"
        });

    }


    catch (error) {

        console.error(
            error
        );


        loadingState.classList.add(
            "hidden"
        );


        emptyState.classList.remove(
            "hidden"
        );


        resultStatus.textContent =
            "ERROR";


        showError(
            error.message ||
            "Something went wrong."
        );

    }


    finally {

        resetButton();

    }

}


// =========================================================
// GENERATE BUTTON
// =========================================================

generateButton.addEventListener(
    "click",
    generateImage
);


// =========================================================
// CMD + ENTER
// =========================================================

promptInput.addEventListener(
    "keydown",
    event => {

        if (
            (
                event.metaKey ||
                event.ctrlKey
            ) &&
            event.key === "Enter"
        ) {

            generateImage();

        }

    }
);


// =========================================================
// COPY PROMPT
// =========================================================

copyPromptButton.addEventListener(
    "click",
    async () => {

        const prompt =
            resultPrompt.textContent;


        if (
            !prompt ||
            prompt === "—"
        ) {

            return;

        }


        try {

            await navigator.clipboard.writeText(
                prompt
            );


            copyPromptButton.textContent =
                "Copied!";


            setTimeout(
                () => {

                    copyPromptButton.textContent =
                        "Copy Prompt";

                },
                1500
            );

        }

        catch (error) {

            console.error(
                error
            );

        }

    }
);


// =========================================================
// REGENERATE
// =========================================================

regenerateButton.addEventListener(
    "click",
    () => {

        if (
            !resultPrompt.textContent ||
            resultPrompt.textContent === "—"
        ) {

            return;

        }


        promptInput.value =
            resultPrompt.textContent;


        characterCount.textContent =
            `${promptInput.value.length} / 10000`;


        generateImage();

    }
);


// =========================================================
// LOAD HISTORY
// =========================================================

async function loadHistory() {

    try {

        const response =
            await fetch(
                `${API_BASE}/api/history`
            );


        const result =
            await response.json();


        if (
            !response.ok ||
            !result.success
        ) {

            throw new Error(
                result.error ||
                "Unable to load history."
            );

        }


        renderHistory(
            result.images || []
        );

    }

    catch (error) {

        console.error(
            "History error:",
            error
        );

    }

}


// =========================================================
// RENDER HISTORY
// =========================================================

function renderHistory(images) {

    const oldCards =
        historyGrid.querySelectorAll(
            ".history-card"
        );


    oldCards.forEach(
        card => card.remove()
    );


    if (
        !images ||
        images.length === 0
    ) {

        historyEmpty.classList.remove(
            "hidden"
        );

        return;

    }


    historyEmpty.classList.add(
        "hidden"
    );


    images.forEach(
        item => {

            const card =
                document.createElement(
                    "div"
                );


            card.className =
                "history-card";


            // -----------------------------------------
            // IMAGE
            // -----------------------------------------

            const imageContainer =
                document.createElement(
                    "div"
                );


            imageContainer.className =
                "history-image";


            const image =
                document.createElement(
                    "img"
                );


            image.src =
                `${API_BASE}${item.image}`;


            image.alt =
                "Generated AI artwork";


            image.loading =
                "lazy";


            // -----------------------------------------
            // OVERLAY
            // -----------------------------------------

            const overlay =
                document.createElement(
                    "div"
                );


            overlay.className =
                "history-overlay";


            // -----------------------------------------
            // VIEW
            // -----------------------------------------

            const viewButton =
                document.createElement(
                    "button"
                );


            viewButton.type =
                "button";


            viewButton.className =
                "history-action";


            viewButton.textContent =
                "View";


            viewButton.addEventListener(
                "click",
                () => {

                    generatedImage.src =
                        image.src;


                    imageResult.classList.remove(
                        "hidden"
                    );


                    emptyState.classList.add(
                        "hidden"
                    );


                    loadingState.classList.add(
                        "hidden"
                    );


                    resultStatus.textContent =
                        "HISTORY";


                    resultPrompt.textContent =
                        "Previously generated image";


                    resultStyle.textContent =
                        "History";


                    resultResolution.textContent =
                        item.resolution ||
                        `${item.width} × ${item.height}`;


                    resultFormat.textContent =
                        item.format;


                    resultSize.textContent =
                        formatFileSize(
                            item.size
                        );


                    resultTime.textContent =
                        "Previously generated";


                    resultSeed.textContent =
                        "—";


                    downloadButton.href =
                        image.src;


                    downloadButton.download =
                        item.filename;


                    imageResult.scrollIntoView({
                        behavior: "smooth",
                        block: "center"
                    });

                }
            );


            // -----------------------------------------
            // DOWNLOAD
            // -----------------------------------------

            const download =
                document.createElement(
                    "a"
                );


            download.className =
                "history-action";


            download.textContent =
                "Download";


            download.href =
                image.src;


            download.download =
                item.filename;


            // -----------------------------------------
            // ADD BUTTONS
            // -----------------------------------------

            overlay.appendChild(
                viewButton
            );


            overlay.appendChild(
                download
            );


            // -----------------------------------------
            // IMAGE
            // -----------------------------------------

            imageContainer.appendChild(
                image
            );


            imageContainer.appendChild(
                overlay
            );


            // -----------------------------------------
            // INFO
            // -----------------------------------------

            const info =
                document.createElement(
                    "div"
                );


            info.className =
                "history-info";


            const filename =
                document.createElement(
                    "span"
                );


            filename.className =
                "history-filename";


            filename.textContent =
                item.filename;


            filename.title =
                item.filename;


            const size =
                document.createElement(
                    "span"
                );


            size.className =
                "history-size";


            size.textContent =
                `${item.resolution} · ${formatFileSize(item.size)}`;


            info.appendChild(
                filename
            );


            info.appendChild(
                size
            );


            // -----------------------------------------
            // CARD
            // -----------------------------------------

            card.appendChild(
                imageContainer
            );


            card.appendChild(
                info
            );


            historyGrid.appendChild(
                card
            );

        }
    );

}


// =========================================================
// REFRESH HISTORY
// =========================================================

refreshHistoryButton.addEventListener(
    "click",
    async () => {

        refreshHistoryButton.disabled =
            true;


        refreshHistoryButton.textContent =
            "↻ Loading...";


        await loadHistory();


        refreshHistoryButton.disabled =
            false;


        refreshHistoryButton.textContent =
            "↻ Refresh";

    }
);


// =========================================================
// CLEAR HISTORY
// =========================================================

clearHistoryButton.addEventListener(
    "click",
    async () => {

        const confirmed =
            confirm(
                "Are you sure you want to delete all generated images?"
            );


        if (!confirmed) {

            return;

        }


        try {

            clearHistoryButton.disabled =
                true;


            clearHistoryButton.textContent =
                "Clearing...";


            const response =
                await fetch(
                    `${API_BASE}/api/history/clear`,
                    {
                        method:
                            "DELETE"
                    }
                );


            const result =
                await response.json();


            if (
                !response.ok ||
                !result.success
            ) {

                throw new Error(
                    result.error ||
                    "Could not clear history."
                );

            }


            await loadHistory();


            clearHistoryButton.textContent =
                "Cleared!";


            setTimeout(
                () => {

                    clearHistoryButton.textContent =
                        "Clear History";

                },
                1200
            );

        }


        catch (error) {

            console.error(
                error
            );


            showError(
                error.message ||
                "Could not clear history."
            );

            clearHistoryButton.textContent =
                "Clear History";

        }


        finally {

            clearHistoryButton.disabled =
                false;

        }

    }
);


// =========================================================
// INITIAL LOAD
// =========================================================

loadHistory();