package Models;

public class Particle {
    private double x, y, theta;
    private final int id;
    private double c,s;

    public Particle(double x, double y, double theta, int id) {
        this.x = x;
        this.y = y;
        this.theta = theta;
        this.id = id;
    }

    public int getId() { return id; }
    public double getX(){
        return x;
    }

     public double getY(){
        return y;
    }

     public double getTheta(){
        return theta;
    }

    public void setX(double x){
        this.x=x;
    }

     public void setY(double y){
        this.y=y;
    }

     public void setTheta(double theta){
        this.theta=theta;
    }

    public void registerCloseParticle(Particle p) {
        c += Math.cos(p.getTheta());
        s += Math.sin(p.getTheta());
    }
    public static void registerCloseParticles(Particle p1, Particle p2){ //! suma atomica
        p1.registerCloseParticle(p2);
        p2.registerCloseParticle(p1);
    }

    public double getMeanAngle ( double N) {
        return Math.atan2(s/N, c/N);
    }

    public void resetMeanAngle() {
        c = 0.0;
        s = 0.0;
    }

    public double vx(double v) { return v * Math.cos(theta); }
    public double vy(double v) { return v * Math.sin(theta); }
}
