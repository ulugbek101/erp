function togglePasswordVisibility(toggleIcon="toggleIcon", fieldId) {
	const passwordField = document.getElementById(fieldId);
	const icon = document.getElementById(toggleIcon);

	if (passwordField.type === "password") {
		passwordField.type = "text";
		icon.innerText = "visibility_off";
	} else {
		passwordField.type = "password";
		icon.innerText = "visibility";
	}
}
