const BASE_URL = "https://banking-api-uy2e.onrender.com/api/v1/banking";

async function requestUserData(username) {
    return fetch(`${BASE_URL}/${username}`)
        .then(response => response.json())
        .catch(error => console.log(error));
}

async function requestRegistration(username, email, password) {
    return fetch(`${BASE_URL}/register/${username}/${email}/${password}`)
        .then(response => response.json())
        .catch(error => console.log(error));
}

function displayData(data, username) {
    const usernameElement = document.getElementById("username");
    const emailElement = document.getElementById("email");
    usernameElement.innerHTML = username;
    emailElement.innerText = data[username][2];
}

// Redirect user
function redirect(url) {
    window.location.href = url;
}

async function requestBalance(username) {
    return fetch(`${BASE_URL}/${username}/balance`)
        .then((response) => response.json())
        .then((data) => displayBalance(data))
        .catch((error) => console.log(error));
}

function displayBalance(data) {
    const balanceElement = document.getElementById("balance");
    balanceElement.innerText = `$${data["Balance"]}`;
}

async function requestTransactionsTo(username) {
    return fetch(`${BASE_URL}/${username}/transactionst`)
        .then((response) => response.json())
        .then((data) => displayTransTo(data["Transactions_t"]))
        .catch((error) => console.log(error));
}

function displayTransTo(data) {
    const transactionHistoryElement = document.querySelector('.transaction-to-user');

    data.forEach(transaction => {
        const transactionDiv = document.createElement('div');
        transactionDiv.classList.add('transaction', 'transaction-to-user');

        const transDate = document.createElement('p');
        transDate.innerHTML = `<b>Date:</b> ${transaction[1]}`;
        const transFrom = document.createElement('p');
        transFrom.innerHTML = `<b>From:</b> ${transaction[2]}`;
        const transAmount = document.createElement('p');
        transAmount.innerHTML = `<b>Amount:</b> ${transaction[4]}`;

        transactionDiv.appendChild(transDate);
        transactionDiv.appendChild(transFrom);
        transactionDiv.appendChild(transAmount);

        transactionHistoryElement.appendChild(transactionDiv);
    });
}

async function requestTransactionsFrom(username) {
    return fetch(`${BASE_URL}/${username}/transactionsf`)
        .then((response) => response.json())
        .then((data) => displayTransFrom(data["Transactions_f"]))
        .catch((error) => console.log(error));
}

function displayTransFrom(data) {
    const transactionHistoryElement = document.querySelector('.transaction-from-user');

    data.forEach(transaction => {
        const transactionDiv = document.createElement('div');
        transactionDiv.classList.add('transaction', 'transaction-from-user');

        const transDate = document.createElement('p');
        transDate.innerHTML = `<b>Date:</b> ${transaction[1]}`;
        const transTo = document.createElement('p');
        transTo.innerHTML = `<b>To:</b> ${transaction[3]}`;
        const transAmount = document.createElement('p');
        transAmount.innerHTML = `<b>Amount:</b> ${transaction[4]}`;

        transactionDiv.appendChild(transDate);
        transactionDiv.appendChild(transTo);
        transactionDiv.appendChild(transAmount);

        transactionHistoryElement.appendChild(transactionDiv);
    });
}

async function register() {
    let username = document.querySelector("input[name='username']").value;
    let email = document.querySelector("input[name='email']").value;
    let password = document.querySelector("input[name='password']").value;

    let registerData = await requestRegistration(username, email, password);
    if (registerData['Success'][0] == true) {
        console.log('User created')
        sessionStorage.setItem('username', username);
        redirect('index.html');
    } else {
        if (registerData['Success'][0] == false) {
            alert(registerData['Success'][1]);
        }
    }
    
}

async function login() {
    let username = document.querySelector("input[name='username']").value;
    let password = document.querySelector("input[name='password']").value;

    let userData = await requestUserData(username);
    // If the user exists and the password is correct then continue
    if (userData && password == userData[username][3]) {
        sessionStorage.setItem('username', username);
        console.log('redirecting...')
        redirect("index.html");
    } else {
        pswdMsg = document.getElementById("msg");
        pswdMsg.innerText = "Incorrect Username/Password";
    }
}

async function requestMoney(username, receiver, amount) {
    return fetch(`${BASE_URL}/${username}/send/${receiver}/${amount}`)
        .then(response => response.json())
        .catch(error => console.log(error));
}

async function sendMoney() {
    let receiver = document.querySelector("input[name='receiver']").value;
    let amount = document.querySelector("input[name='amount']").value;
    let userName = sessionStorage.getItem("username");

    if (amount >= 0) {
        let sendAmount = await requestMoney(userName, receiver, amount);
        if (sendAmount['Success'][0] == true) {
            console.log('test');
            alert("Money sent successfully");
            redirect('index.html');
        } else {
            console.log('false');
            if (sendAmount['Success'][0] == false) {
                alert(sendAmount['Success'][1]);
            }
        }
        
    };


    // If the user exists and the password is correct then continue
    if (userData && password == userData[username][3]) {
        sessionStorage.setItem('username', username);
        console.log('redirecting...')
        redirect("index.html");
    } else {
        pswdMsg = document.getElementById("msg");
        pswdMsg.innerText = "Incorrect Username/Password";
    }
}

function logout() {
    sessionStorage.removeItem('username');
    redirect("login.html");
}

// On page load, get the logged-in user's username and display user info
 window.onload = async function () {

    // Get the relative url
    var pathname = window.location.pathname;

    // Onload behavior is different depending on path
    switch(pathname) {
        case "/client/index.html" :
            // Get the username from session
            let username = sessionStorage.getItem("username");
            username = username ? username : redirect("login.html");

            // Display the user info
            userData = await requestUserData(username);
            displayData(userData, username);
            requestBalance(username);
            break;

        case "/client/login.html" :
            break;
        case "/client/transaction_history.html" :
            // Get the username from session
            let currentUser = sessionStorage.getItem("username");
            currentUser = currentUser ? currentUser : redirect("login.html");

            requestTransactionsTo(currentUser);
            requestTransactionsFrom(currentUser);
            break;
        case "/client/send_money.html" :
            let curUser = sessionStorage.getItem("username");
            curUser = curUser ? curUser : redirect("login.html");
            break;


    }
}
