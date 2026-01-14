"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Search, ChevronRight, Brain, Utensils, Award, Sparkles } from "lucide-react";
import RecipeCard from "@/components/RecipeCard";
import SearchBar from "@/components/SearchBar";
import { API_BASE_URL } from "@/lib/config";

interface Recipe {
  id: number;
  name: string;
  image: string;
}

export default function Home() {
  const [popularRecipes, setPopularRecipes] = useState<Recipe[]>([]);
  const [searchQuery, setSearchQuery] = useState("");

  useEffect(() => {
    // Fetch popular recipes
    fetch(`${API_BASE_URL}/recipes/search`)
      .then((res) => res.json())
      .then((data) => setPopularRecipes(data.items.slice(0, 6)))
      .catch((err) => console.error("Failed to fetch recipes:", err));
  }, []);

  const handleSearch = () => {
    if (searchQuery.trim()) {
      window.location.href = `/search?q=${encodeURIComponent(searchQuery)}`;
    }
  };

  return (
    <div className="home-page">
      {/* Hero Section */}
      <section className="hero-section container">
        <div className="badge animate-fade-in animate-float">
          <Sparkles size={14} />
          <span>Powered by Gemini AI</span>
        </div>

        <h1 className="hero-title animate-fade-in" style={{ animationDelay: '0.1s' }}>
          Master the Art of <br />
          <span className="text-primary-gradient">Intuitive Cooking</span>
        </h1>

        <p className="hero-subtitle animate-fade-in" style={{ animationDelay: '0.2s' }}>
          No recipes. No instructions. Just your culinary instincts.
          Guess ingredients, unlock AI hints, and prove you're a Master Chef.
        </p>

        {/* Search Bar */}
        <div className="search-container animate-fade-in" style={{ animationDelay: '0.3s' }}>
          <div className="search-wrapper-v2">
            <SearchBar
              value={searchQuery}
              onChange={setSearchQuery}
              onSearch={handleSearch}
              placeholder="What do you want to cook today?"
              showButton={true}
            />
          </div>
          <div className="search-suggestions">
            <span>Try:</span>
            <Link href="/search?q=Pasta">Pasta</Link>
            <Link href="/search?q=Sushi">Sushi</Link>
            <Link href="/search?q=Taco">Tacos</Link>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="features-section">
        <div className="container">
          <div className="section-header">
            <h2 className="section-title">How It Works</h2>
            <p className="section-subtitle">Three steps to culinary mastery</p>
          </div>

          <div className="features-grid">
            <div className="feature-card animate-fade-in" style={{ animationDelay: '0.4s' }}>
              <div className="feature-icon-wrapper">
                <Brain size={32} />
              </div>
              <h3>Choose a Challenge</h3>
              <p>Pick a famous dish from our AI-curated library. You'll see the name and a picture, but nothing else.</p>
            </div>

            <div className="feature-card animate-fade-in" style={{ animationDelay: '0.5s' }}>
              <div className="feature-icon-wrapper">
                <Utensils size={32} />
              </div>
              <h3>Guess Ingredients</h3>
              <p>Type in what you think goes into the dish. Unlock sensory hints if you get stuck!</p>
            </div>

            <div className="feature-card animate-fade-in" style={{ animationDelay: '0.6s' }}>
              <div className="feature-icon-wrapper">
                <Award size={32} />
              </div>
              <h3>Get Rated</h3>
              <p>Our AI Chef evaluates your intuition and accuracy, giving you a score out of 100 based on your choices.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Popular Challenges Section */}
      <section className="challenges-section container">
        <div className="section-header flex-between">
          <div>
            <h2 className="section-title">Popular Challenges</h2>
            <p className="section-subtitle">The most attempted puzzles this week</p>
          </div>
          <Link href="/search" className="btn-secondary d-sm-inline">
            Explore All
          </Link>
        </div>

        <div className="grid-layout">
          {popularRecipes.length > 0 ? (
            popularRecipes.map((recipe, index) => (
              <RecipeCard
                key={recipe.id}
                id={recipe.id}
                name={recipe.name}
                image={recipe.image}
                style={{ animationDelay: `${0.7 + (index * 0.1)}s` }}
              />
            ))
          ) : (
            // Skeleton loader or empty state
            Array(6).fill(0).map((_, i) => (
              <div key={i} className="recipe-card-skeleton glass-panel" />
            ))
          )}
        </div>

        <div className="mobile-only-btn">
          <Link href="/search" className="btn-primary full-width">
            <span>Explore All</span>
            <ChevronRight size={18} />
          </Link>
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta-section container">
        <div className="cta-card glass-panel">
          <div className="cta-content">
            <h2>Ready to Test Your Instincts?</h2>
            <p>Join thousands of aspiring cooks and master the art of intuition.</p>
            <Link href="/search" className="navbar-cta">
              <Sparkles size={18} />
              <span>Start Your First Puzzle</span>
            </Link>
          </div>
          <div className="cta-decoration animate-float-slow" aria-hidden="true">
            <Utensils size={120} />
          </div>
        </div>
      </section>
    </div>
  );
}
