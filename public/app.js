const menuGrid = document.querySelector("#menu-grid");
const reservationForm = document.querySelector("#reservation-form");
const formMessage = document.querySelector("#form-message");
const dateInput = reservationForm.querySelector('[name="date"]');
const navToggle = document.querySelector(".nav-toggle");
const mainNav = document.querySelector(".main-nav");

function localDateString() {
  const today = new Date();
  const month = String(today.getMonth() + 1).padStart(2, "0");
  const day = String(today.getDate()).padStart(2, "0");
  return `${today.getFullYear()}-${month}-${day}`;
}

dateInput.min = localDateString();

function renderMenuItem(item) {
  const card = document.createElement("article");
  card.className = "menu-card";

  const image = document.createElement("img");
  image.src = item.image_url;
  image.alt = item.name;
  image.loading = "lazy";

  const category = document.createElement("p");
  category.className = "menu-category";
  category.textContent = item.category;

  const title = document.createElement("h3");
  title.textContent = item.name;

  const description = document.createElement("p");
  description.className = "menu-description";
  description.textContent = item.description;

  const price = document.createElement("span");
  price.className = "menu-price";
  price.textContent = `$${Number(item.price).toFixed(2)}`;

  const details = document.createElement("div");
  details.className = "menu-card-details";
  details.append(category, title, description, price);
  card.append(image, details);
  return card;
}

async function loadMenu() {
  try {
    const response = await fetch("/api/menu");
    if (!response.ok) throw new Error("Menu service unavailable");
    const items = await response.json();
    if (!Array.isArray(items) || items.length === 0) {
      menuGrid.innerHTML = '<p class="menu-status">Our menu is being updated. Please check back soon.</p>';
      return;
    }
    menuGrid.replaceChildren(...items.map(renderMenuItem));
  } catch {
    menuGrid.innerHTML = '<p class="menu-status">We could not load the menu right now. Please try again in a moment.</p>';
  }
}

reservationForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const submitButton = reservationForm.querySelector('button[type="submit"]');
  const formData = new FormData(reservationForm);
  const values = Object.fromEntries(formData.entries());

  submitButton.disabled = true;
  submitButton.textContent = "Sending request…";
  formMessage.className = "form-message";
  formMessage.textContent = "";

  try {
    const response = await fetch("/api/reservations", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(values),
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || "We couldn't send your request.");
    formMessage.className = "form-message success";
    formMessage.textContent = `${result.message} We'll be in touch to confirm.`;
    reservationForm.reset();
    dateInput.min = localDateString();
  } catch (error) {
    formMessage.className = "form-message error";
    formMessage.textContent = error.message || "Something went wrong. Please try again.";
  } finally {
    submitButton.disabled = false;
    submitButton.innerHTML = 'Request a table <span aria-hidden="true">↗</span>';
  }
});

navToggle.addEventListener("click", () => {
  const isOpen = navToggle.getAttribute("aria-expanded") === "true";
  navToggle.setAttribute("aria-expanded", String(!isOpen));
  mainNav.classList.toggle("is-open", !isOpen);
});

mainNav.addEventListener("click", (event) => {
  if (event.target.closest("a")) {
    navToggle.setAttribute("aria-expanded", "false");
    mainNav.classList.remove("is-open");
  }
});

loadMenu();
