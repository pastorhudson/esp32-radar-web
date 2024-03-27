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
    // Convert standalone URLs into clickable links
    markdown = markdown.replace(/(\b(https?|ftp|file):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|])/ig, '<a href="$1" target="_blank" class="text-blue-500 hover:text-blue-700 transition duration-300 ease-in-out">$1</a>');

    // Convert Markdown links to HTML <a> tags with Tailwind styling
    let html = markdown.replace(/\[([^\]]+)\]\((https?:\/\/[^\s]+)\)/g, '<a href="$2" target="_blank" class="text-blue-500 hover:text-blue-700 transition duration-300 ease-in-out">$1</a>');

    // Convert text surrounded by ** to bold with Tailwind styling (optional)
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong class="font-bold">$1</strong>');

    // Convert Markdown headers (## example) to HTML <h2> tags with Tailwind styling
    html = html.replace(/^##\s?(.+)/gm, '<h2 class="text-2xl font-semibold mt-4 mb-2">$1</h2>');

    // Convert Markdown bulleted lists to HTML <ul> and <li> with Tailwind styling
    html = html.replace(/(\n\*\s.+(?:\n\*.+)*)/g, function(match) {
        let items = match.trim().split('\n');
        let listItems = items.map(item => `<li class="ml-4 list-disc">${item.substring(2)}</li>`).join('');
        return `<ul class="list-outside pl-5 mt-2 mb-2">${listItems}</ul>`;
    });

    // Optionally, handle line breaks with spacing instead of <br>, considering Tailwind and modern web practices

    return html;
}
