import React from 'react';
import './App.css';
import {Link} from 'react-router-dom';
function Nav() {
  return (
    <nav>
      <h1>Formulyntio</h1>
      <ul className="nav-links">
        <Link to="/predict">
          <li><h1>Predict</h1></li>  
        </Link>

        <Link to="/documentation">
          <li><h1>Documentation</h1></li>
        </Link>
      </ul>
    </nav>
  )
}

export default Nav;