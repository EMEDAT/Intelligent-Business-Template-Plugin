import React, { useState } from 'react';
import styles from '../styles/components.module.scss';

const Header = () => {
  const [menuOpen, setMenuOpen] = useState(false);

  const toggleMenu = () => setMenuOpen(!menuOpen);

  return (
    <header className={styles.header}>
      <img src="/logo.jpg" alt="Logo" className={styles.logo} />
      <nav>
        <button onClick={toggleMenu} className={styles.menuButton}>
          ☰
        </button>
        <ul className={`${styles.navLinks} ${menuOpen ? styles.showMenu : ''}`}>
          <li><a href="/">Home</a></li>
          <li><a href="/about">About</a></li>
          <li><a href="/contact">Contact</a></li>
          <li><a href="/templateGeneration">Generate Template</a></li>
        </ul>
      </nav>
    </header>
  );
};

export default Header;
