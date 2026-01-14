import Link from "next/link";
import Image from "next/image";
import { ChefHat, ChevronRight } from "lucide-react";

interface RecipeCardProps {
    id: number;
    name: string;
    image: string;
    className?: string;
    style?: React.CSSProperties;
    height?: string | number;
    children?: React.ReactNode;
}

export default function RecipeCard({ id, name, image, className = "", style, height = "240px", children }: RecipeCardProps) {
    return (
        <Link href={`/recipe/${id}`} className={`recipe-card animate-fade-in ${className}`} style={style}>
            <div className="recipe-image-wrapper" style={{ position: 'relative', height: height, width: '100%' }}>
                <Image
                    src={image}
                    alt={name}
                    fill
                    style={{ objectFit: 'cover' }}
                />
                <div className="card-badge">
                    <ChefHat size={16} color="var(--primary)" /> Puzzle
                </div>
            </div>
            <div className="recipe-content">
                <h3 className="recipe-card-title">{name}</h3>

                {children ? children : (
                    <div className="recipe-card-footer">
                        <div className="difficulty-indicator">
                            <span className="dot success" />
                            <span>Ready to Play</span>
                        </div>
                        <div className="card-cta-btn">
                            Challenge <ChevronRight size={14} />
                        </div>
                    </div>
                )}
            </div>
        </Link>
    );
}
