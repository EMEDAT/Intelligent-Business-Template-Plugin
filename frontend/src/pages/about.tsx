import React from 'react'
import Header from '../components/Header'
import Footer from '../components/Footer'
import styles from '../styles/Home.module.scss'

const About = () => {
  return (
    <div className={styles.pageContainer}>
      <Header />
      <main className={styles.mainContent}>
        <h1>About the Business Template Plugin</h1>
        <p>
          This tool automatically generates customizable business templates and plans, saving you time and effort
          during business decision-making.
        </p>
      </main>
      <Footer />
    </div>
  )
}

export default About
