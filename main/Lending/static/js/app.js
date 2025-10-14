$(document).ready(function () {
    "use strict";

    function isWebp() {
        function testWebP(callback) {
            let webP = new Image;
            webP.onload = webP.onerror = function () {
                callback(webP.height == 2);
            };
            webP.src = "data:image/webp;base64,UklGRjoAAABXRUJQVlA4IC4AAACyAgCdASoCAAIALmk0mk0iIiIiIgBoSygABc6WWgAA/veff/0PP8bA//LwYAAA";
        }
        testWebP((function (support) {
            let className = support === true ? "webp" : "no-webp";
            document.documentElement.classList.add(className);
        }));
    }

    let addWindowScrollEvent = false;
    setTimeout((() => {
        if (addWindowScrollEvent) {
            let windowScroll = new Event("windowScroll");
            window.addEventListener("scroll", (function () {
                document.dispatchEvent(windowScroll);
            }));
        }
    }), 0);

    $('#policy').on('change', function () {
        $('#button-end-model-quiz').prop('disabled', !this.checked);
    });
    $('#button-end-model-quiz').prop('disabled', !$('#policy').prop('checked'));

    const btnNext = document.getElementById("btn-next");
    const titleAll = document.getElementById("title-quiz");
    const quizSlider = document.getElementById("quiz-slider");
    const quizSliderEnd = document.getElementById("quiz-end");
    const quizPreloader = document.querySelector(".quiz__preloader");

    btnNext.addEventListener("click", function () {
        titleAll.classList.add("quiz-active");
        quizSlider.classList.add("quiz-slider-active");
        quizSliderEnd.classList.add("quiz-slider-active");
        quizPreloader.classList.add("quiz-preloader-active");
    });

    const phone = document.getElementById("phone");
    const whatapp = document.getElementById("whatapp");
    const tg = document.getElementById("tg");
    const input = document.getElementById("contact-form");
    let status = true;

    phone.onclick = function () {
        status = true;
        input.placeholder = "Введите Ваш телефон";
        input.type = "tel";
        input.value = "";
    };
    whatapp.onclick = function () {
        status = true;
        input.placeholder = "Введите Ваш WhatsApp";
        input.type = "tel";
        input.value = "";
    };
    tg.onclick = function () {
        status = false;
        input.placeholder = "Введите Ваш Telegram";
        input.type = "text";
        input.value = "";
    };

    input.addEventListener('input', function (e) {
        if (status) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length > 11) value = value.substring(0, 11);
            let formattedValue = '+7 (';
            if (value.length > 1) formattedValue += value.substring(1, 4);
            if (value.length > 4) formattedValue += ') ' + value.substring(4, 7);
            if (value.length > 7) formattedValue += '-' + value.substring(7, 9);
            if (value.length > 9) formattedValue += '-' + value.substring(9, 11);
            e.target.value = formattedValue;
        }
    });

    const popups = document.querySelectorAll(".popup");
    const popupButton = document.querySelectorAll(".header__social, .header__tel-text");
    const body = document.body;
    const popupWrapper = document.querySelectorAll(".popup__wrapper");
    const fixBlock = document.querySelectorAll(".fix-block");
    let paddingOffset = window.innerWidth - document.body.offsetWidth + "px";
    let marginOffset = document.body.offsetWidth - window.innerWidth + "px";

    function openPopup(elem) {
        elem.classList.add("popup-open");
        body.classList.add("lock");
        document.body.style.paddingRight = paddingOffset;
        fixBlock.forEach(el => el.style.paddingRight = paddingOffset);
        popupWrapper.forEach(el => el.style.marginLeft = marginOffset);
    }

    function closePopup(e) {
        if (e.target.classList.contains("popup__close") || e.target.closest(".popup__close") || e.target.classList.contains("popup__wrapper")) {
            e.target.closest(".popup").classList.remove("popup-open");
            body.classList.remove("lock");
            document.body.style.paddingRight = "0px";
            fixBlock.forEach(el => el.style.paddingRight = "0px");
            popupWrapper.forEach(el => el.style.marginLeft = "auto");
        }
    }

    popupButton.forEach(btn => {
        btn.addEventListener("click", e => {
            let data = e.target.dataset.popupOpen;
            popups.forEach(popup => {
                if (popup.dataset.popup == data || popup.dataset.popup == e.target.closest(".header__social, .header__tel-text").dataset.popupOpen)
                    openPopup(popup);
            });
        });
    });

    popups.forEach(popup => popup.addEventListener("click", e => closePopup(e)));

    function initSliders() {
        if (document.querySelector(".quiz__slider")) new Swiper(".quiz__slider", {
            slidesPerView: 1,
            spaceBetween: 200,
            autoHeight: true,
            speed: 1100,
            allowTouchMove: false,
            navigation: {
                prevEl: ".quiz-button-prev",
                nextEl: ".quiz-button-next"
            }
        });
    }
    initSliders();

    // ======= hardest slider =======
    const hardestMainSlider = document.querySelector(".hardest-slider");
    const hardestMainImage = hardestMainSlider.querySelector("img");
    const hardestPrevBtn = document.querySelector(".hardest-prev-btn");
    const hardestNextBtn = document.querySelector(".hardest-next-btn");
    const hardestThumbnails = document.querySelectorAll(".hardest-thumbnail");
    const hardestDescription = document.querySelector(".hardest-description");

    const hardestSliderData = examples.map(example => ({
        mainImage: example.images[0].url,
        thumbnails: example.images.map(img => img.url),
        description: example.text
    }));

    const hardestSliderDataMobile = examples.map(example => ({
        mainImage: example.images[0].mobaleUrl,
        thumbnails: example.images.map(img => img.mobaleUrl),
        description: example.text
    }));

    const getCurrentSliderData = () => window.innerWidth <= 768 ? hardestSliderDataMobile : hardestSliderData;
    let hardestCurrentSliderIndex = 0;
    let hardestCurrentImageIndex = 0;

    function updateHardestSlider(index) {
        const sliderData = getCurrentSliderData();
        const slider = sliderData[index];
        hardestMainImage.src = slider.thumbnails[0];
        hardestCurrentImageIndex = 0;
        if (window.innerWidth <= 11768) {
            hardestDescription.innerHTML = slider.description;
            hardestDescription.style.display = "block";
        }
        hardestThumbnails.forEach((thumb, i) => {
            if (sliderData[i] === undefined) {
                thumb.remove();
            } else {
                const img = thumb.querySelector("img");
                if (img) img.src = sliderData[i].mainImage;
                thumb.classList.toggle("active", i === index);
            }
        });
    }

    hardestThumbnails.forEach((thumb, index) => {
        thumb.addEventListener("click", () => {
            const sliderData = getCurrentSliderData();
            hardestThumbnails.forEach(t => t.classList.remove("active"));
            thumb.classList.add("active");
            hardestCurrentSliderIndex = index;
            hardestCurrentImageIndex = 0;
            const currentSlider = sliderData[hardestCurrentSliderIndex];
            hardestMainImage.src = currentSlider.thumbnails[hardestCurrentImageIndex];
            if (window.innerWidth <= 11768) hardestDescription.innerHTML = currentSlider.description;
        });
    });

    function showPrevImage() {
        const sliderData = getCurrentSliderData();
        const currentSlider = sliderData[hardestCurrentSliderIndex];
        if (hardestCurrentImageIndex === 0) {
            hardestCurrentSliderIndex = (hardestCurrentSliderIndex - 1 + sliderData.length) % sliderData.length;
            const newSlider = sliderData[hardestCurrentSliderIndex];
            hardestCurrentImageIndex = newSlider.thumbnails.length - 1;
            hardestMainImage.src = newSlider.thumbnails[hardestCurrentImageIndex];
            hardestThumbnails.forEach((thumb, i) => {
                thumb.classList.toggle("active", i === hardestCurrentSliderIndex);
                thumb.querySelector("img").src = sliderData[i].mainImage;
            });
            if (window.innerWidth <= 11768) hardestDescription.innerHTML = newSlider.description;
        } else {
            hardestCurrentImageIndex--;
            hardestMainImage.src = currentSlider.thumbnails[hardestCurrentImageIndex];
        }
    }

    function showNextImage() {
        const sliderData = getCurrentSliderData();
        const currentSlider = sliderData[hardestCurrentSliderIndex];
        if (hardestCurrentImageIndex === currentSlider.thumbnails.length - 1) {
            hardestCurrentSliderIndex = (hardestCurrentSliderIndex + 1) % sliderData.length;
            const newSlider = sliderData[hardestCurrentSliderIndex];
            hardestCurrentImageIndex = 0;
            hardestMainImage.src = newSlider.thumbnails[hardestCurrentImageIndex];
            hardestThumbnails.forEach((thumb, i) => {
                thumb.classList.toggle("active", i === hardestCurrentSliderIndex);
            });
            if (window.innerWidth <= 11768) hardestDescription.innerHTML = newSlider.description;
        } else {
            hardestCurrentImageIndex++;
            hardestMainImage.src = currentSlider.thumbnails[hardestCurrentImageIndex];
        }
    }

    hardestPrevBtn.addEventListener("click", showPrevImage);
    hardestNextBtn.addEventListener("click", showNextImage);

    // ======= touch/swipe support =======
    let touchStartX = 0;
    let touchEndX = 0;

    hardestMainSlider.addEventListener("touchstart", (e) => {
        touchStartX = e.changedTouches[0].screenX;
    });

    hardestMainSlider.addEventListener("touchend", (e) => {
        touchEndX = e.changedTouches[0].screenX;
        handleSwipe();
    });

    function handleSwipe() {
        const swipeThreshold = 50;
        if (touchEndX < touchStartX - swipeThreshold) {
            showNextImage();
        }
        if (touchEndX > touchStartX + swipeThreshold) {
            showPrevImage();
        }
    }

    window.addEventListener("resize", () => {
        updateHardestSlider(hardestCurrentSliderIndex);
    });

    updateHardestSlider(0);
    window["FLS"] = true;
    isWebp();
});
