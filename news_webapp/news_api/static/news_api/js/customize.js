

document.addEventListener('DOMContentLoaded', function() {
    const customizeButton = document.getElementById("customizeButton");
    const customizeModal = document.getElementById("customizeModal");
    const closeModal = document.getElementById("closeModal");

    // display modal
    customizeButton.onclick = function() {
        customizeModal.style.display = "block";
    }

    // close modal
    closeModal.onclick = function() {
        customizeModal.style.display = "none";
    }
    window.onclick = function(event) {
        if (event.target == customizeModal) {
            customizeModal.style.display = "none";
        }
    }

    // selected category
    const categoryButtons = document.querySelectorAll('.category-btn');
    categoryButtons.forEach(button => {
        button.addEventListener('click', function() {
            button.classList.toggle('selected');
        });
    });


    document.getElementById("customize-form").addEventListener("submit", function(event) {
        event.preventDefault();

        const selectedCategories = Array.from(document.querySelectorAll('.category-btn.selected'))
            .map(button => button.getAttribute('data-value'));

        fetch('/foryou/save_preferences/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            },
            body: JSON.stringify({
                categories: selectedCategories,
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                customizeModal.style.display = "none";

                updateCategoryNews(data.category_news);
            } else {
                alert('There was an error saving preferences.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('There was an error.');
        });
    });

    function updateCategoryNews(categoryNews) {
        const articlesContainer = document.querySelector('.category-bound');
        if (articlesContainer) {
            articlesContainer.innerHTML = '';
    
            for (const [category, articles] of Object.entries(categoryNews)) {
                const hole = document.createElement('div');
                hole.classList.add('hole');
    
                const categoryLink = document.createElement('a');
                categoryLink.href = `/category/${category}`;
                categoryLink.innerHTML = `
                    <h2 id="category-${category}" class="category">
                        ${category} <i class="bx bx-chevron-right"></i>
                    </h2>
                `;
                hole.appendChild(categoryLink);
    
                articles.forEach(article => {
                    const articleCard = document.createElement('div');
                    articleCard.classList.add('article-card');
                    articleCard.innerHTML = `
                        <div class="title">
                            <!-- <p>${ article.name }</p> -->
                            <!-- <p>${ article.description }</p> -->
                            <a class="news-link" target="_blank" href="${ article.news_url }" data-news-id="${ article.id }">
                            ${ article.title }
                            </a>
                            <p  >${ article.published_at }</p>
                            <p class="views"> Views ${ article.view_count}</p>

                        </div>
                        <div class="image">
                            <img src="${ article.image_url }" alt="" />
                            <!-- <a href="${ article.news_url }">${ article.title }</a> -->
                        </div>
                    `;
                    hole.appendChild(articleCard);
                });
    
                articlesContainer.appendChild(hole);
            }
        } else {
            console.error('Articles container not found.');
        }
    }

});
