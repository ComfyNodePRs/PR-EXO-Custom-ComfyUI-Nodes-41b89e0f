import { app } from "../../../scripts/app.js";
import { ComfyWidgets } from "../../../scripts/widgets.js";

console.log("EXO.DisplayText extension loaded");

// Display input text in the node
app.registerExtension({
    name: "EXO.DisplayText",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "ComfyUI_EXO_DisplayText") {
            function populate(message) {
                console.log("Populate function called with message:", message);
                
                let positiveText = "";
                let negativeText = "";

                if (message && message.text) {
                    // Handle execution message
                    console.log("Processing message.text:", message.text);
                    if (Array.isArray(message.text)) {
                        // Join the character array back into a string and split by newline
                        const fullText = message.text.join('');
                        const parts = fullText.split('\n');
                        positiveText = parts[0] || "";
                        negativeText = parts[1] || "";
                    }
                } else if (Array.isArray(message)) {
                    // Handle direct array input (like widget values)
                    [positiveText, negativeText] = message;
                }

                console.log("Final text values:", {positiveText, negativeText});

                // Clear existing display widgets (keep only input widgets)
                if (this.widgets) {
                    while (this.widgets.length > 2) {  // Keep the first two input widgets
                        this.widgets[this.widgets.length - 1].onRemove?.();
                        this.widgets.pop();
                    }
                }

                // Create display widgets
                const positiveWidget = ComfyWidgets["STRING"](this, "Positive_Display", ["STRING", { multiline: true }], app).widget;
                positiveWidget.inputEl.readOnly = true;
                positiveWidget.inputEl.style.opacity = 0.6;
                positiveWidget.inputEl.style.whiteSpace = 'normal';
                positiveWidget.inputEl.style.wordWrap = 'break-word';
                positiveWidget.inputEl.style.backgroundColor = '#2a2a2a';
                positiveWidget.value = positiveText;
                positiveWidget.inputEl.placeholder = "Positive Text";

                const negativeWidget = ComfyWidgets["STRING"](this, "Negative_Display", ["STRING", { multiline: true }], app).widget;
                negativeWidget.inputEl.readOnly = true;
                negativeWidget.inputEl.style.opacity = 0.6;
                negativeWidget.inputEl.style.whiteSpace = 'normal';
                negativeWidget.inputEl.style.wordWrap = 'break-word';
                negativeWidget.inputEl.style.backgroundColor = '#2a2a2a';
                negativeWidget.value = negativeText;
                negativeWidget.inputEl.placeholder = "Negative Text";

                requestAnimationFrame(() => {
                    const size = this.computeSize();
                    this.onResize?.(size);
                    app.graph.setDirtyCanvas(true, false);
                });
            }

            // Update text on execution
            const onExecuted = nodeType.prototype.onExecuted;
            nodeType.prototype.onExecuted = function (message) {
                console.log("Node executed with message:", message);
                onExecuted?.apply(this, arguments);
                populate.call(this, message);
            };

            const onConfigure = nodeType.prototype.onConfigure;
            nodeType.prototype.onConfigure = function () {
                console.log("Node configured - Full widgets_values:", this.widgets_values);
                
                onConfigure?.apply(this, arguments);
                
                // Ensure we keep the input widgets
                if (this.widgets_values?.length >= 2) {
                    console.log("Attempting to populate with:", this.widgets_values);
                    populate.call(this, this.widgets_values);
                }
            };
        }
    },
});