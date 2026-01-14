"use client";

import { useEffect, useState } from "react";
import Image from "next/image";
import { useParams, useRouter } from "next/navigation";
import { Eye, CheckCircle, AlertTriangle, ChefHat, Sparkles, ChevronLeft, Timer, Trophy, Lightbulb } from "lucide-react";
import Loading from "@/components/Loading";
import { API_BASE_URL } from "@/lib/config";

interface Recipe {
    id: number;
    name: string;
    image: string;
    hints: string[];
    ingredients?: string[];
}

interface ValidationResult {
    score: number;
    feedback: string;
    matched_ingredients: string[];
    all_ingredients: string[];
}

export default function RecipePage() {
    const params = useParams();
    const router = useRouter();
    const id = params.id;

    const [recipe, setRecipe] = useState<Recipe | null>(null);
    const [loading, setLoading] = useState(true);

    const [hintsRevealed, setHintsRevealed] = useState(0);
    const [hintCooldown, setHintCooldown] = useState(0);
    const [plan, setPlan] = useState("");
    const [submitting, setSubmitting] = useState(false);
    const [result, setResult] = useState<ValidationResult | null>(null);

    useEffect(() => {
        fetch(`${API_BASE_URL}/recipes/${id}`)
            .then(res => res.json())
            .then(data => setRecipe(data))
            .catch(err => console.error(err))
            .finally(() => setLoading(false));
    }, [id]);

    useEffect(() => {
        let interval: NodeJS.Timeout;
        if (hintCooldown > 0) {
            interval = setInterval(() => {
                setHintCooldown((prev) => prev - 1);
            }, 1000);
        }
        return () => clearInterval(interval);
    }, [hintCooldown]);

    const handleRevealHint = () => {
        if (recipe && hintsRevealed < recipe.hints.length && hintCooldown === 0) {
            setHintsRevealed(prev => prev + 1);
            setHintCooldown(10);
        }
    };

    const handleSubmit = async () => {
        if (!plan.trim()) return;
        setSubmitting(true);
        setResult(null);

        try {
            const res = await fetch(`${API_BASE_URL}/recipes/validate`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    recipe_id: Number(id),
                    plan: plan,
                    hints_used: hintsRevealed
                })
            });

            if (!res.ok) throw new Error(`Status: ${res.status}`);
            const data = await res.json();
            setResult(data);
            window.scrollTo({ top: 0, behavior: 'smooth' });
        } catch (err: any) {
            console.error(err);
            setResult({
                score: 0,
                feedback: "Chef seems busy right now. Please try again.",
                matched_ingredients: [],
                all_ingredients: recipe?.ingredients || []
            });
        } finally {
            setSubmitting(false);
        }
    };

    if (loading) return <Loading />;
    if (!recipe) return <div className="no-results container"><h3>Challenge Not Found</h3><button className="btn btn-secondary mt-4" onClick={() => router.push('/search')}>Back to Challenges</button></div>;

    const currentPotential = 100 - (hintsRevealed * 6);

    return (
        <div className="recipe-detail-wrapper">
            {/* Dark background overlay for hero */}
            <div className="hero-background-glow" style={{ backgroundImage: `url(${recipe.image})` }} />

            <div className="container z-1">
                {/* Back Button */}
                <button
                    className="back-btn animate-fade-in"
                    onClick={() => router.back()}
                >
                    <ChevronLeft size={20} />
                    <span>Back to library</span>
                </button>

                {/* Hero Card */}
                <div className="recipe-hero-card glass-panel animate-fade-in" style={{ animationDelay: '0.1s' }}>
                    <div className="hero-main">
                        <div className="hero-image-container">
                            <Image src={recipe.image} alt={recipe.name} fill className="hero-img" priority />
                            <div className="card-badge premium-badge">
                                <Sparkles size={16} />
                                <span>AI Puzzle</span>
                            </div>
                        </div>
                        <div className="hero-content">
                            <header className="hero-header">
                                <div className="difficulty-tag">Medium Difficulty</div>
                                <h1 className="hero-recipe-title text-primary-gradient">{recipe.name}</h1>
                                <p className="hero-recipe-desc">Analyze the visuals, decode the flavors, and describe the master method.</p>
                            </header>

                            <div className="hero-stats">
                                <div className="hero-stat-item">
                                    <div className="stat-icon-box score"><Trophy size={18} /></div>
                                    <div className="stat-info">
                                        <span className="label">Current Potential</span>
                                        <span className="value success">{currentPotential} pts</span>
                                    </div>
                                </div>
                                <div className="hero-stat-item">
                                    <div className="stat-icon-box hints"><Lightbulb size={18} /></div>
                                    <div className="stat-info">
                                        <span className="label">Hints Used</span>
                                        <span className="value primary">{hintsRevealed} / {recipe.hints.length}</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div className="recipe-game-grid mt-4">

                    {/* HINTS PANEL */}
                    <div className="glass-panel hint-exploration-panel animate-fade-in" style={{ animationDelay: '0.2s' }}>
                        <div className="panel-header">
                            <h2 className="panel-title"><Sparkles size={22} className="primary-icon" /> Sensory Hints</h2>
                            <p className="panel-subtitle">Insights from the Chef's kitchen</p>
                        </div>

                        <div className="hints-list">
                            {recipe.hints.map((hint, idx) => {
                                const isRevealed = idx < hintsRevealed;
                                return (
                                    <div key={idx} className={`hint-item-v2 ${isRevealed ? 'revealed' : 'hidden'}`}>
                                        <div className="hint-num">{idx + 1}</div>
                                        <div className="hint-text">
                                            {isRevealed ? hint : "???"}
                                        </div>
                                        {!isRevealed && <div className="lock-overlay"><Eye size={14} /> Encrypted</div>}
                                    </div>
                                );
                            })}
                        </div>

                        {hintsRevealed < recipe.hints.length && !result && (
                            <button
                                className={`reveal-hint-btn ${hintCooldown > 0 ? 'loading' : ''}`}
                                onClick={handleRevealHint}
                                disabled={hintCooldown > 0}
                            >
                                {hintCooldown > 0 ? (
                                    <><Timer size={18} /> Recharging ({hintCooldown}s)</>
                                ) : (
                                    <>Consume Hint <span className="pts-cost">-6 pts</span></>
                                )}
                            </button>
                        )}
                    </div>

                    {/* INTERACTION PANEL */}
                    <div className="glass-panel interaction-panel animate-fade-in" style={{ animationDelay: '0.3s' }}>
                        {result ? (
                            <div className="verdict-display">
                                <div className="verdict-header">
                                    <div className={`verdict-score-ring ${result.score >= 80 ? 'gold' : result.score >= 50 ? 'silver' : 'bronze'}`}>
                                        <div className="score-num">{result.score}</div>
                                        <div className="score-total">/ 100</div>
                                    </div>
                                    <h2 className="verdict-title">Chef's Decision</h2>
                                    <div className="feedback-statement">{result.feedback}</div>
                                </div>

                                <div className="ingredients-check">
                                    <h3 className="sub-title">Ingredient Profiling</h3>
                                    <div className="chips-container">
                                        {result.all_ingredients.map(ing => {
                                            const matched = result.matched_ingredients.includes(ing);
                                            return (
                                                <div key={ing} className={`ing-chip ${matched ? 'matched' : 'missed'}`}>
                                                    {matched ? <CheckCircle size={14} /> : <AlertTriangle size={14} />}
                                                    {ing}
                                                </div>
                                            );
                                        })}
                                    </div>
                                </div>

                                <button className="btn btn-primary w-full mt-4" onClick={() => window.location.reload()}>
                                    Challenge Again
                                </button>
                                <button className="btn btn-secondary w-full mt-2" onClick={() => router.push('/search')}>
                                    Try Different Dish
                                </button>
                            </div>
                        ) : (
                            <div className="input-display">
                                <div className="panel-header">
                                    <h2 className="panel-title"><ChefHat size={22} className="primary-icon" /> The Cooking Plan</h2>
                                    <p className="panel-subtitle">Define ingredients and steps</p>
                                </div>

                                <textarea
                                    className="plan-textarea"
                                    value={plan}
                                    onChange={(e) => setPlan(e.target.value)}
                                    placeholder="Describe your process... (e.g. 'I'd start by braising the beef in red wine...')"
                                />

                                <div className="input-footer">
                                    <p className="input-hint">The Chef considers accuracy, technique, and ingredients.</p>
                                    <button
                                        className="btn btn-primary submit-plan-btn"
                                        onClick={handleSubmit}
                                        disabled={submitting || !plan.trim()}
                                    >
                                        {submitting ? "Chef is Tasting..." : "Present to Chef"}
                                    </button>
                                </div>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}
