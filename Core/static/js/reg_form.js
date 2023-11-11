const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');

signUpButton.addEventListener('click', () => {
	container.classList.add("right-panel-active");
});

signInButton.addEventListener('click', () => {
	container.classList.remove("right-panel-active");
});





const { useState, useEffect } = React;

function DevLoginSumbit(props) {
	
	const [ReactLoginValidErrorText, setReactLoginValidErrorText] = useState("");

	// валидация логина
	const validate_login_form = () => {
		
		var log_form = document.getElementById("send-data-login");
			
		let login = log_form.querySelector('[name="username"]').value;
		let passwd = log_form.querySelector('[name="password"]').value;
		
		console.log(login, passwd)

		if (passwd.length >= 5 && login.length >= 4) {
			log_form.submit();
		} else {
			let error = ""
			
			if (passwd.length < 5 && login.length < 4)
				error = "Длинна пароля должна быть больше 5 символов, логина больше 4.";
			else if (passwd == "" || login == "") {
				if (passwd == "")
					error += "Поле пароль должно быть заполнено";
				if (login == "")
					error += "Поле логина должно быть заполнено";
			}
			else if (passwd.length < 5)
				error = "Длинна пароля должна быть больше 5 символов.";

			else if (login.length < 4)
				error = "Длинна логина должна быть больше 5 символов.";
			

			setReactLoginValidErrorText(error)
		}


	
	
	
		
		
	};
	
	// signInButton.addEventListener(() => {
	// 	alert("")
	// });

	return ( 
		<div>
				<div>
					<p class="ErrorMessage">{ReactLoginValidErrorText}</p>
				</div>
				<button type="button" class="clr-1" onClick={validate_login_form}>Вход</button>
		</div>
	)
}

ReactDOM.createRoot(
	document.getElementById("login_error")
)
.render(
	<DevLoginSumbit />
);



function DevRegisterSumbit(props) {
	
	const [ReactRegisterValidErrorText, setReactRegisterValidErrorText] = useState("");

	// валидация логина
	const validate_register_form = () => {
		
	let reg_form = document.getElementById("send-data-register");
	
	let login = reg_form.querySelector('[name="username"]').value;
	let passwd1 = reg_form.querySelector('[name="password"]').value;
	let passwd2 = reg_form.querySelector('[name="password1"]').value;
	
	console.log(login, passwd1, passwd2)
	
	if (passwd1.length >= 5 && passwd2.length >= 5 && passwd1 == passwd2) {
		reg_form.submit();
	} 
	else {
		var error = ""
		
		if (login.length <= 5) {
			error += "Логин должен быть длины больше 4. "
		}

		if (passwd1.length <= 5 || passwd2.length <= 5) 
			error += "Пароли должны быть длины больше 5. ";	
			
		if (passwd1 != passwd2)
			error += "Пароли дожны совпадать. "
		};

		setReactRegisterValidErrorText(error);
	}

	return ( 
		<div>
				<div>
					<p class="ErrorMessage">{ReactRegisterValidErrorText}</p>
				</div>
				<button class="clr-1" type="button" onClick={validate_register_form}>Зарегистрироваться</button>

		</div>
	)
};

ReactDOM.createRoot(
	document.getElementById("register_error")
)
.render(
	<DevRegisterSumbit />
);

