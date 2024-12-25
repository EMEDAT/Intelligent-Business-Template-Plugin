import React from 'react'
import styles from '../styles/components.module.scss';

type TemplateCardProps = {
  title: string
  description: string
}

const TemplateCard: React.FC<TemplateCardProps> = ({ title, description }) => {
  return (
    <div className={styles.templateCard}>
      <h2>{title}</h2>
      <p>{description}</p>
      <button>Use Template</button>
    </div>
  )
}

export default TemplateCard
