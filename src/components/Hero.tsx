import { Cloud, TrendingDown } from "lucide-react";

const Hero = () => {
  return (
    <section id="home" className="pt-24 pb-12 px-4 relative overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-br from-primary/10 via-secondary/5 to-background -z-10" />
      
      {/* Floating Elements */}
      <div className="absolute top-20 left-10 opacity-20 animate-float">
        <Cloud className="h-16 w-16 text-primary" />
      </div>
      <div className="absolute top-40 right-20 opacity-20 animate-float" style={{ animationDelay: "1s" }}>
        <Cloud className="h-12 w-12 text-secondary" />
      </div>
      <div className="absolute bottom-20 right-40 opacity-20 animate-float" style={{ animationDelay: "2s" }}>
        <Cloud className="h-20 w-20 text-primary" />
      </div>

      <div className="container mx-auto max-w-6xl text-center animate-fade-in">
        <div className="inline-flex items-center gap-2 px-4 py-2 bg-primary/10 rounded-full mb-6">
          <TrendingDown className="h-4 w-4 text-primary" />
          <span className="text-sm font-medium text-primary">Predicting Air Quality for 2025</span>
        </div>

        <h1 className="text-5xl md:text-7xl font-bold mb-6 bg-gradient-to-r from-primary via-secondary to-primary bg-clip-text text-transparent leading-tight">
          Air Quality Prediction System
        </h1>

        <p className="text-xl md:text-2xl text-muted-foreground mb-8 max-w-3xl mx-auto">
          Advanced machine learning model analyzing historical data from 2020-2024 to predict air quality metrics for a cleaner future.
        </p>

        <div className="flex flex-wrap justify-center gap-4 text-sm md:text-base">
          <div className="bg-card rounded-lg px-6 py-3 shadow-md">
            <div className="text-2xl font-bold text-primary">5 Years</div>
            <div className="text-muted-foreground">Historical Data</div>
          </div>
          <div className="bg-card rounded-lg px-6 py-3 shadow-md">
            <div className="text-2xl font-bold text-secondary">7 Parameters</div>
            <div className="text-muted-foreground">Weather & Pollutants</div>
          </div>
          <div className="bg-card rounded-lg px-6 py-3 shadow-md">
            <div className="text-2xl font-bold text-primary">Real-time</div>
            <div className="text-muted-foreground">AQI Predictions</div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;
