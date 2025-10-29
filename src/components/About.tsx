import { Card } from "@/components/ui/card";
import { Database, Brain, Target, Award } from "lucide-react";

const About = () => {
  const features = [
    {
      icon: Database,
      title: "Comprehensive Dataset",
      description: "5 years of historical air quality data from 2020-2024, covering multiple weather parameters and pollutant levels.",
    },
    {
      icon: Brain,
      title: "Machine Learning Model",
      description: "Advanced ML algorithms trained on historical patterns to predict AQI with high accuracy for 2025.",
    },
    {
      icon: Target,
      title: "Multi-Parameter Analysis",
      description: "Analyzes temperature, humidity, wind speed, NO₂, CO, PM2.5, and PM10 for comprehensive predictions.",
    },
    {
      icon: Award,
      title: "Real-time Predictions",
      description: "Instant AQI predictions with color-coded categories from Good to Hazardous for easy interpretation.",
    },
  ];

  return (
    <section id="about" className="py-16 px-4 bg-muted/30">
      <div className="container mx-auto max-w-6xl">
        <div className="text-center mb-12 animate-fade-in">
          <h2 className="text-4xl font-bold mb-4 text-foreground">
            About This Project
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Leveraging data science to predict and improve air quality for healthier communities
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-6 mb-12">
          {features.map((feature, index) => {
            const Icon = feature.icon;
            return (
              <Card 
                key={index}
                className="p-6 hover:shadow-lg transition-all duration-300 animate-slide-in"
                style={{ animationDelay: `${index * 0.1}s` }}
              >
                <div className="flex items-start gap-4">
                  <div className="p-3 bg-primary/10 rounded-lg">
                    <Icon className="h-6 w-6 text-primary" />
                  </div>
                  <div>
                    <h3 className="text-xl font-semibold mb-2 text-foreground">
                      {feature.title}
                    </h3>
                    <p className="text-muted-foreground">
                      {feature.description}
                    </p>
                  </div>
                </div>
              </Card>
            );
          })}
        </div>

        <Card className="p-8 bg-gradient-to-br from-primary/5 to-secondary/5 border-2 border-primary/20 animate-fade-in">
          <div className="text-center">
            <h3 className="text-2xl font-bold mb-4 text-foreground">
              Project Methodology
            </h3>
            <div className="max-w-3xl mx-auto space-y-4 text-muted-foreground text-left">
              <p>
                This Air Quality Prediction System uses machine learning to analyze historical environmental data and predict future air quality indices. The model was trained on comprehensive datasets spanning 2020-2024, incorporating weather conditions and pollutant measurements.
              </p>
              <p>
                The system considers multiple factors including temperature, humidity, wind speed, and key pollutants (NO₂, CO, PM2.5, PM10) to generate accurate AQI predictions. These predictions help communities prepare for poor air quality conditions and take preventive measures.
              </p>
              <p className="font-semibold text-foreground">
                Built with modern web technologies including React, TypeScript, and Tailwind CSS, powered by advanced machine learning algorithms.
              </p>
            </div>
          </div>
        </Card>

        <div className="text-center mt-12">
          <p className="text-muted-foreground">
            Created with passion for environmental sustainability and public health
          </p>
          <p className="text-sm text-muted-foreground mt-2">
            © 2025 Sky Forecast Hub. Data visualization powered by Recharts.
          </p>
        </div>
      </div>
    </section>
  );
};

export default About;
