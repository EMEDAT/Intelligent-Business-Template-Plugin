import React from 'react'
import Header from '../components/Header'
import Footer from '../components/Footer'
import styles from '../styles/Home.module.scss'


const Contact = () => {
  return (
    <div className={styles.pageContainer}>
      <Header />
      <main className={styles.mainContent}>
        <h1>Contact Us</h1>
        <p>Email: ThePillarApp.com</p>
        <p>Phone: (+234) 706 905 6828</p>
      </main>
      <Footer />
    </div>
  )
}

export default Contact
