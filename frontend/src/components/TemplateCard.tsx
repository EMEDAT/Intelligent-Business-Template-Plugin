import React from 'react'
import styles from '../styles/components.module.scss';

type TemplateCardProps = {
  title: string;
  description: string;
  isSelected: boolean;
  onSelect: () => void;
};

const TemplateCard: React.FC<TemplateCardProps> = ({ title, description, isSelected, onSelect }) => {
  return (
    <div
      className={`${styles.templateCard} ${isSelected ? styles.selectedCard : ''}`}
      onClick={onSelect}
    >
      <h2>{title}</h2>
      <p>{description}</p>
      <button>Use Template</button>
    </div>
  );
};

export default TemplateCard;
