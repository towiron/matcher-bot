const tg = window.Telegram.WebApp;
tg.expand();

const cityInput = document.getElementById("cityInput");
const detectLocationBtn = document.getElementById("detectLocationBtn");

let userLatitude = null;
let userLongitude = null;

// 🔹 Функция обратного геокодирования через OpenStreetMap
async function reverseGeocode(latitude, longitude) {
  try {
    const response = await fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${latitude}&lon=${longitude}&zoom=10`);
    const data = await response.json();

    if (data.address) {
      const cityName = data.address.city || data.address.town || data.address.village || data.address.municipality || data.address.state;

      if (cityName) {
        cityInput.value = cityName;
        userLatitude = latitude;
        userLongitude = longitude;
      } else {
        alert("Не удалось определить город");
      }
    }
  } catch (error) {
    console.error("Error reverse geocoding:", error);
    alert("Ошибка при определении города. Введите вручную.");
  }
}

// 🔹 Обработка кнопки
detectLocationBtn.addEventListener("click", () => {
  if (!navigator.geolocation) {
    alert("Геолокация не поддерживается в вашем браузере");
    return;
  }

  detectLocationBtn.disabled = true;
  detectLocationBtn.textContent = "⏳ Определение...";

  navigator.geolocation.getCurrentPosition(
    async (position) => {
      const { latitude, longitude } = position.coords;

      // 🔄 Вызываем встроенную геолокацию через nominatim напрямую
      await reverseGeocode(latitude, longitude);

      detectLocationBtn.disabled = false;
      detectLocationBtn.textContent = "📍 Определить город";
    },
    (error) => {
      alert("Ошибка геолокации: " + error.message);
      detectLocationBtn.disabled = false;
      detectLocationBtn.textContent = "📍 Определить город";
    }
  );
});

// 🔹 Отправка формы
document.getElementById("profileForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const formData = Object.fromEntries(new FormData(e.target).entries());

  formData.has_children = formData.has_children === "true";
  if (formData.polygamy) {
    formData.polygamy = formData.polygamy === "true";
  }

  const payload = {
    action: 'profile_submit',
    ...formData,
    user_id: tg.initDataUnsafe?.user?.id,
    latitude: userLatitude,
    longitude: userLongitude
  };

  console.log("Отправка данных в бота:", payload); // ← Проверь это тоже

  // 📤 Отправка в Telegram-бот
  tg.sendData(JSON.stringify(payload)); // ← сюда доходит?
  alert("Данные отправлены!");
});
