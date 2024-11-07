document
	.getElementById("table-search")
	.addEventListener("keydown", function (event) {
		// Check if Enter key (keyCode 13 or 'Enter') is pressed
		if (event.key === "Enter") {
			event.preventDefault(); // Prevent default form submission behavior
			const query = this.value.trim(); // Get the input value and trim whitespace

			// Prevent submission if the input is empty or just spaces
			if (query.length === 0) {
				console.log("Input is empty or just whitespace. Submission prevented.");
				return; // Exit the function early if the input is invalid
			}

			// Create a URL with the query as a GET parameter
			const url = new URL(window.location.href);
			url.searchParams.set("search", query); // 'search' is the query param name

			// Redirect to the URL with the new query
			window.location.href = url.toString();
		}
	});
