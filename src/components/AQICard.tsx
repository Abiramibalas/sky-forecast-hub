import { Card } from "@/components/ui/card";
import { AlertCircle, CheckCircle, AlertTriangle, XCircle, Skull } from "lucide-react";

interface AQICardProps {
  aqi: number;
  category: string;
  explanation?: string;
}

const AQICard = ({ aqi, category, explanation }: AQICardProps) => {
  const getAQIColor = (category: string) => {
    const colors: Record<string, string> = {
      Good: "hsl(var(--aqi-good))",
      Moderate: "hsl(var(--aqi-moderate))",
      Poor: "hsl(var(--aqi-poor))",
      "Very Poor": "hsl(var(--aqi-very-poor))",
      Hazardous: "hsl(var(--aqi-hazardous))",
    };
    return colors[category] || colors.Good;
  };

  const getIcon = (category: string) => {
    const icons: Record<string, React.ReactNode> = {
      Good: <CheckCircle className="h-16 w-16" />,
      Moderate: <AlertCircle className="h-16 w-16" />,
      Poor: <AlertTriangle className="h-16 w-16" />,
      "Very Poor": <XCircle className="h-16 w-16" />,
      Hazardous: <Skull className="h-16 w-16" />,
    };
    return icons[category] || icons.Good;
  };

  const getDescription = (category: string) => {
    const descriptions: Record<string, string> = {
      Good: "Air quality is satisfactory and poses little or no health risk.",
      Moderate: "Air quality is acceptable for most individuals.",
      Poor: "Sensitive groups may experience health effects.",
      "Very Poor": "Health alert: everyone may experience health effects.",
      Hazardous: "Health warning: emergency conditions affecting the entire population.",
    };
    return descriptions[category] || descriptions.Good;
  };

  return (
    <Card 
      className="p-8 h-full flex flex-col justify-center animate-scale-in shadow-xl"
      style={{ borderColor: getAQIColor(category), borderWidth: '2px' }}
    >
      <div className="text-center">
        <div 
          className="inline-flex p-4 rounded-full mb-4 animate-float"
          style={{ backgroundColor: `${getAQIColor(category)}20` }}
        >
          <div style={{ color: getAQIColor(category) }}>
            {getIcon(category)}
          </div>
        </div>

        <h3 className="text-2xl font-bold mb-2 text-foreground">Air Quality Index</h3>
        
        <div className="mb-4">
          <div 
            className="text-6xl font-bold mb-2"
            style={{ color: getAQIColor(category) }}
          >
            {aqi}
          </div>
          <div 
            className="text-2xl font-semibold px-4 py-2 rounded-full inline-block"
            style={{ 
              backgroundColor: `${getAQIColor(category)}20`,
              color: getAQIColor(category)
            }}
          >
            {category}
          </div>
        </div>

        <p className="text-muted-foreground leading-relaxed">
          {getDescription(category)}
        </p>

        {explanation && (
          <div className="mt-4 p-4 bg-muted/50 rounded-lg border-l-4 border-primary">
            <h4 className="font-semibold text-sm mb-2 text-foreground">Analysis:</h4>
            <p className="text-sm text-muted-foreground leading-relaxed">
              {explanation}
            </p>
          </div>
        )}

        <div className="mt-6 pt-6 border-t border-border">
          <div className="grid grid-cols-5 gap-2 text-xs">
            <div className="text-center">
              <div className="h-2 bg-[hsl(var(--aqi-good))] rounded mb-1" />
              <span className="text-muted-foreground">Good</span>
            </div>
            <div className="text-center">
              <div className="h-2 bg-[hsl(var(--aqi-moderate))] rounded mb-1" />
              <span className="text-muted-foreground">Moderate</span>
            </div>
            <div className="text-center">
              <div className="h-2 bg-[hsl(var(--aqi-poor))] rounded mb-1" />
              <span className="text-muted-foreground">Poor</span>
            </div>
            <div className="text-center">
              <div className="h-2 bg-[hsl(var(--aqi-very-poor))] rounded mb-1" />
              <span className="text-muted-foreground">Very Poor</span>
            </div>
            <div className="text-center">
              <div className="h-2 bg-[hsl(var(--aqi-hazardous))] rounded mb-1" />
              <span className="text-muted-foreground">Hazardous</span>
            </div>
          </div>
        </div>
      </div>
    </Card>
  );
};

export default AQICard;
