/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import Wysiwyg from 'web_editor.wysiwyg';
import OpenAIGenerateContentDialog from 'ai_web_editor.OpenAIGenerateContentDialog';

const p = text => {
    const p = document.createElement('p');
    p.innerText = text;
    return p;
}

Wysiwyg.include({
    _getPowerboxOptions: function () {
        const options = this._super.apply(this, arguments);
        const {commands, categories} = options;
        categories.push({ name: 'OpenAI', priority: 40 });
        commands.push(...[
            {
                category: 'OpenAI',
                name: 'Generate Content',
                priority: 10,
                description: 'Produce Content with the Aid of AI',
                fontawesome: 'fa-align-justify',
                isDisabled: () => !this.odooEditor.isSelectionInBlockRoot(),
                callback: async () => {
                    this.generateContent();
                },
            },
        ]);
        return {...options, commands, categories};
    },
    generateContent() {
        const selection = this.odooEditor.document.getSelection();
        const range = selection.rangeCount && selection.getRangeAt(0);
        const targetNode = range && range.startContainer;

        const targetElement = targetNode && targetNode.nodeType === Node.ELEMENT_NODE
            ? targetNode
            : targetNode && targetNode.parentNode;
        
        const contentDialog = new OpenAIGenerateContentDialog(this, {}, targetElement);
        contentDialog.open();
    },
});