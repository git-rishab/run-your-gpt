import styles from "../styles/navbar.module.css";
import { useNavigate } from "react-router-dom";
import { notification } from "../notification";

export default function Navbar() {
  const loggedIn = sessionStorage.getItem('token');
  const redirect = useNavigate();
  const handleLogout = ()=>{
    sessionStorage.clear();
    notification('Logout Succesfull', '', 'white', '#F44336')
    redirect('/')
  }
  return (
    <nav className={styles.nav}>
      <div className={styles.logo} onClick={()=>redirect('/')}>
        Logo
      </div>
      <div>
        <div onClick={()=>redirect('/')}>Home</div>
      {
        loggedIn ? <div><div className={styles.login} onClick={()=>redirect('/dashboard')}>Dashboard</div><div onClick={handleLogout}>Logout</div></div> : <><div onClick={()=>redirect('/login')}>Login</div><div onClick={()=>redirect('/register')}>Signup</div></>
      } 
      </div>
    </nav>
  )
}
