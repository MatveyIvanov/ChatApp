window.onload = function () {
	var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
	$.ajax({
		url: 'auth',
		data: { 'auth_type': 'signin' },
		type: 'post',
		beforeSend: function (xhr) {
			xhr.setRequestHeader('X-CSRFToken', csrftoken);
		},
		success: function (data) {
			$('.sign-in-container').html(data);

			document.querySelector('#signin_submit').onclick = signInSubmitButtonClick;
			initInputs();
		}
	});
}

const signUpButton = document.querySelector('#signUp');
const signInButton = document.querySelector('#signIn');
const container = document.querySelector('#container');

function initInputs() {
	signin_id = document.querySelector('#signin_id');
	signin_password = document.querySelector('#signin_password');
	if (signin_id && signin_password) {
		signin_id.onkeyup = function (e) {
			if (e.keyCode === 13) {  // enter, return
				document.querySelector('#signin_submit').click();
			}
		};
		signin_password.onkeyup = function (e) {
			if (e.keyCode === 13) {  // enter, return
				document.querySelector('#signin_submit').click();
			}
		};
	}

	signup_id = document.querySelector('#signup_id');
	signup_password1 = document.querySelector('#signup_password1');
	signup_password2 = document.querySelector('#signup_password2');
	if (signup_id && signup_password1 && signup_password2) {
		signup_id.onkeyup = function (e) {
			if (e.keyCode === 13) {  // enter, return
				document.querySelector('#signup_submit').click();
			}
		};
		signup_password1.onkeyup = function (e) {
			if (e.keyCode === 13) {  // enter, return
				document.querySelector('#signup_submit').click();
			}
		};
		signup_password2.onkeyup = function (e) {
			if (e.keyCode === 13) {  // enter, return
				document.querySelector('#signup_submit').click();
			}
		};
	}
}

signUpButton.addEventListener('click', () => {
	container.classList.add("right-panel-active");
	var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
	$.ajax({
		url: 'auth',
		data: { 'auth_type': 'signup' },
		type: 'post',
		beforeSend: function (xhr) {
			xhr.setRequestHeader('X-CSRFToken', csrftoken);
		},
		success: function (data) {
			$('.sign-up-container').html(data);

			document.querySelector('#signup_submit').onclick = signUpSubmitButtonClick;
			initInputs();
		}
	});
});

signInButton.addEventListener('click', () => {
	container.classList.remove("right-panel-active");
	var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
	$.ajax({
		url: 'auth',
		data: { 'auth_type': 'signin' },
		type: 'post',
		beforeSend: function (xhr) {
			xhr.setRequestHeader('X-CSRFToken', csrftoken);
		},
		success: function (data) {
			$('.sign-in-container').html(data);

			document.querySelector('#signin_submit').onclick = signInSubmitButtonClick;
			initInputs();
		}
	});
});

function signUpSubmitButtonClick() {
	var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
	$.ajax({
		url: 'auth',
		type: 'post',
		data: $('#signup_form').serialize() + "&submit=signup",
		beforeSend: function (xhr) {
			xhr.setRequestHeader('X-CSRFToken', csrftoken);

			document.querySelector('#signup_id').className = "auth-input";
			document.querySelector('#signup_id_error_message').innerHTML = "";
			document.querySelector('#signup_password1').className = "auth-input";
			document.querySelector('#signup_password1_error_message').innerHTML = "";
			document.querySelector('#signup_password2').className = "auth-input";
			document.querySelector('#signup_password2_error_message').innerHTML = "";
		},
		success: function (data) {
			window.location.replace(data['redirect_url']);
		},
		error: function (error) {
			if (error.responseJSON.type == 'id') {
				document.querySelector('#signup_id').className += " err";
				document.querySelector('#signup_id_error_message').innerHTML = error.responseJSON.error_message;
			}
			else {
				document.querySelector('#signup_password1').className += " err";
				document.querySelector('#signup_password1_error_message').innerHTML = error.responseJSON.error_message;
				document.querySelector('#signup_password2').className += " err";
				document.querySelector('#signup_password2_error_message').innerHTML = error.responseJSON.error_message;
			}
		}
	});
};

function signInSubmitButtonClick() {
	var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
	$.ajax({
		url: 'auth',
		type: 'post',
		data: $('#signin_form').serialize() + "&submit=signin",
		beforeSend: function (xhr) {
			xhr.setRequestHeader('X-CSRFToken', csrftoken);

			document.querySelector('#signin_id').className = "auth-input";
			document.querySelector('#signin_id_error_message').innerHTML = "";
			document.querySelector('#signin_password').className = "auth-input";
			document.querySelector('#signin_password_error_message').innerHTML = "";
		},
		success: function (data) {
			window.location.replace(data['redirect_url']);
		},
		error: function (error) {
			if (error.responseJSON.type == 'id') {
				document.querySelector('#signin_id').className += " err";
				document.querySelector('#signin_id_error_message').innerHTML = error.responseJSON.error_message;
			}
			else {
				document.querySelector('#signin_password').className += " err";
				document.querySelector('#signin_password_error_message').innerHTML = error.responseJSON.error_message;
			}
		}
	});
};