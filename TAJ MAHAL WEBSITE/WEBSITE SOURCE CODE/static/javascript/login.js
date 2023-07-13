const signup = document.querySelector(".signup");
const login = document.querySelector(".login");
const movebtn = document.querySelector(".movebtn");

login.addEventListener("click",()=>{
    movebtn.classList.add("rightbtn");
})

signup.addEventListener("click",()=>{
    movebtn.classList.remove("rightbtn");
})

<div class="box">
                        <form action="{{ url_for('home') }}" method="post">
                            <div class="msg">{{ msg }}</div>
                            <h2>NAME</h2>
                            <div class="data">
                            <input type="name" name="username" placeholder="" id="username">
                            <h3>GMAIL</h3>
                            <input type="gmail" name="gmail" placeholder="" id="gmail" >
                            <h3>PASSWORD</H3>
                            <input type="password" name="password" placeholder="" id ="password">
                            </div>
                            <div class="ua">
                                <h4>Already hava an account<a href="login" class="us">LOGIN</a></h4>
                            </div>
                            <input type="submit" class="text" onclick="register()"  value="REGISTER">            
                        </form>
                    </div>
            </div>
        </div>


        .wrapper
{
    margin-top: 100px;
    margin-left: 700px;
    display: flex;
    position: fixed;
    justify-content: center;
    align-items: center;

}
.modelform
{
    position: absolute;
    width: 900px;
    min-height: 150px;
    background: linear-gradient( to right,white,deepskyblue);
    border: 5px solid black;
    border-radius: 50px;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    
}
.actionbtns
{
    width: 80%;
    background: linear-gradient(to right,deeppink,white);
    margin: 1px;
    display: flex;
    border-radius: 50px;
    justify-content: space-between;
    position: relative;

}
.actionbtn
{
    padding: 1em;
    width: 50%;
    outline: none;
    border: none;
    border-radius: 50px;
    background-color: transparent;
    color: darkmagenta;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
}
.movebtn
{
    position: absolute;
    width: 50%;
    height: 90%;
    margin: 2px;
    outline: none;
    border-radius: 50px;
    background: linear-gradient(to left,#fff,yellow);
    color: deeppink;
    font-size: 14px;
    font-weight: 600;
    transform:translateX(0);
    transition: all 0.2s ease-in-out;
}
.rightbtn
{
    transform:translateX(98%);
    transition: all 0.2s ease-in-out;
}
.modelform .pic img
{
    position: absolute;
    right: 500px;
}
form h2
{
    position: absolute;
    margin-left: 380px;
    margin-top: 5px;
    color: darkblue;
}
form h3
{
    position: absolute;
    margin-top:6px;
    margin-left: 380px;
    color: darkblue;
}
.data input
{
    margin-top: 40px;
    margin-left: 400px;
    border: none;
    outline: none;
    border-bottom: 3px solid darkblue;
    padding: 4px 70px;
    font-weight: 800;
    background: none;
    color: green;
    font-size: 15px;
}
.data input:hover
{
    background: linear-gradient(to left);
}
.text
{
    color: white;
    margin-left: 380px;
    background: linear-gradient(to right,deeppink,deepskyblue);
    padding: 12px 15px;
    border-radius: 10px;
}
.text:hover
{
    transition: 1.5s;

}
.ua
{
    color:darkblue;
    font-size: 15px;
    margin-left: 380px;
}
.us
{
    margin-left: 3px;
    color: darkred;
    text-decoration: none;
    font-family: 'Times New Roman', Times, serif;
}
.us:hover
{
    font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
}

