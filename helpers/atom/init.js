// reverse words in text lines in the active editor
atom.commands.add('atom-text-editor', 'custom:reverse-words-in-line', () => {
  const editor = atom.workspace.getActiveTextEditor();
  if (!editor) return;

  // Create a checkpoint so 'Undo' reverts the whole operation at once
  const checkpoint = editor.createCheckpoint();

  // Process line by line to handle Arabic/RTL and LTR correctly
  const text = editor.getText().split("\n")
    .map(line => {
      // Split by any whitespace, reverse, and join back
      return line.trim().split(/\s+/).reverse().join(" ");
    })
    .join("\n");

  editor.setText(text);
  editor.groupChangesSinceCheckpoint(checkpoint);
});
