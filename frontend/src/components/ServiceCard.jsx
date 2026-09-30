import { ArrowRight } from "lucide-react";

function ServiceCard({ icon, title, description, action, onClick }) {
  return (
    <div className="service-card">
      <div className="service-icon">
        {icon}
      </div>

      <h3>{title}</h3>

      <p>{description}</p>

      <button className="service-action" onClick={onClick}>
        {action}
        <ArrowRight size={17} />
      </button>
    </div>
  );
}

export default ServiceCard;