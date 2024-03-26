document.addEventListener('DOMContentLoaded', function() {
    fetch('/storage/FormationFlight-latest-release-bin-assets/release.txt')
    .then(response => response.text())
    .then(data => {
        const releaseData = parseReleaseData(data);
        const versionElement = document.getElementById('release-version');
        const notesContentElement = document.getElementById('notes-content');
        const releaseNotesDiv = document.getElementById('release-notes');

        if (versionElement) versionElement.innerText = releaseData.version;
        if (notesContentElement) notesContentElement.innerHTML = markdownToHtml(releaseData.notes);
        if (releaseNotesDiv) releaseNotesDiv.style.display = 'none'; // Hide notes by default
    });

    document.getElementById('toggleNotes').addEventListener('click', function() {
        const notesDiv = document.getElementById('release-notes');
        if (notesDiv) {
            notesDiv.style.display = (notesDiv.style.display === 'none') ? 'block' : 'none';
            this.textContent = (notesDiv.style.display === 'none') ? 'Show Release Notes' : 'Hide Release Notes';
        }
    });
});

function parseReleaseData(data) {
    const lines = data.split('\n');
    const version = lines[0];
    let notes = lines.slice(2).join('\n'); // Join starting from the third line to keep line breaks
    return { version, notes: notes.trim() };
}

function markdownToHtml(markdown) {
    // Convert Markdown links to HTML <a> tags
    let html = markdown.replace(/\[([^\]]+)\]\((https?:\/\/[^\s]+)\)/g, '<a href="$2" target="_blank">$1</a>');

    // Convert Markdown headers (## example) to HTML <h2> tags
    html = html.replace(/^##\s?(.+)/gm, '<h2>$1</h2>');

    // Replace line breaks with <br> for proper formatting
    html = html.replace(/\n/g, '<br>');

    return html;
}
