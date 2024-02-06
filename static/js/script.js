
// JavaScript for filtering data
const searchInput = document.getElementById('searchInput');
const cardContainer = document.getElementById('cardContainer');
const noResultsMessage = document.getElementById('noResultsMessage');

searchInput.addEventListener('input', function () {
    const searchValue = searchInput.value.toLowerCase();

    let found = false;

    for (const card of cardContainer.getElementsByClassName('card')) {
        const name = card.getElementsByClassName('card-title')[0].textContent.toLowerCase();
        const description = card.getElementsByClassName('card-text')[0].textContent.toLowerCase();
        const keywords = card.getElementsByClassName('keywords')[0].textContent.toLowerCase();

        if (name.includes(searchValue) || description.includes(searchValue) || keywords.includes(searchValue)) {
            card.style.display = 'inline-block';
            found = true;
        } else {
            card.style.display = 'none';
        }
    }

    // Show/hide "No results found" message
    if (found) {
        noResultsMessage.style.display = 'none';
    } else {
        noResultsMessage.style.display = 'block';
    }
});

// Add this in your script.js file or within a script tag in your HTML
function openModal(eventName, eventInfo, keywords) {
    document.getElementById("modalEventName").innerText = eventName;
    document.getElementById("modalEventInfo").innerText = eventInfo;
    document.getElementById("modalKeywords").innerText = keywords;
    $('#myModal').modal('show');
}

function closeModal() {
    $('#myModal').modal('hide');
}


