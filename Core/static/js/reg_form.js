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

let servererrorlogin = ""

function DevLoginSumbit(props) {
	
	const [ReactLoginValidErrorText, setReactLoginValidErrorText] = useState(servererrorlogin);

	//  Выполнить действия при загрузке страницы
	useEffect(() => {
		let login_button = document.getElementById('login_button');
		console.log(login_button);
		login_button.addEventListener('click', validate_login_form);
		
	  }, []);

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

	return ( 
		<p class="ErrorMessage">{ReactLoginValidErrorText}</p>
	)
}

ReactDOM.createRoot(
	document.getElementById("login_error")
)
.render(
	<DevLoginSumbit />
);


let servererrorregistration = ""

function DevRegisterSumbit(props) {
	
	const [ReactRegisterValidErrorText, setReactRegisterValidErrorText] = useState(servererrorregistration);

	//  Выполнить действия при загрузке страницы
	useEffect(() => {
		// достаем кнопку из DOM модели
		let reg_button = document.getElementById('reg_button');
		console.log(reg_button);
		// добавляем обработчик события
		reg_button.addEventListener('click', validate_register_form);
		
	  }, []);

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
		<p class="ErrorMessage">{ReactRegisterValidErrorText}</p>
	)
};

ReactDOM.createRoot(
	document.getElementById("register_error")
)
.render(
	<DevRegisterSumbit />
);

