let currentSlide = 0;
const slides = document.querySelectorAll(".onboarding-slide");
const nextBtn = document.getElementById("next-btn");
const prevBtn = document.getElementById("prev-btn");
const skipBtn = document.getElementById("skip-btn");

// Exibir slide atual
function showSlide(index) {
    slides.forEach((slide, i) => {
        slide.style.display = i === index ? "block" : "none";
    });
}

// Avançar slide
nextBtn.addEventListener("click", () => {
    if (currentSlide < slides.length - 1) {
        currentSlide++;
        showSlide(currentSlide);
    } else {
        closeOnboarding();
    }
});

// Voltar slide
prevBtn.addEventListener("click", () => {
    if (currentSlide > 0) {
        currentSlide--;
        showSlide(currentSlide);
    }
});

// Pular onboarding
skipBtn.addEventListener("click", closeOnboarding);

// Fechar onboarding e redirecionar para a página principal
function closeOnboarding() {
    localStorage.setItem("onboardingComplete", "true");
    window.location.href = "index.html";
}

// Verificar se o onboarding já foi visto
if (localStorage.getItem("onboardingComplete")) {
    window.location.href = "index.html";
} else {
    showSlide(currentSlide);
}
