import streamlit as st
import pandas as pd
import math

# ============================================================
# SMART NON-CONTACT RADAR LEVEL TRANSMITTER ENGINEERING ASSISTANT
# Harini M - Streamlit Ultimate Version
# ============================================================

class RadarApplication:
    def __init__(self, dk, foam_mm, vapour, distance_m, oil_layer_cm):
        self.dk = dk
        self.foam_mm = foam_mm
        self.vapour = vapour
        self.distance_m = distance_m
        self.oil_layer_cm = oil_layer_cm

class SignalBudget:
    def __init__(self, app, frequency, antenna):
        self.app = app
        self.frequency = frequency
        self.antenna = antenna

    def suitability_score(self):
        score = 100

        # Dielectric Constant
        if self.app.dk < 2:
            score -= 25
        elif self.app.dk < 5:
            score -= 10

        # Foam
        if self.app.foam_mm > 300:
            score -= 25
        elif self.app.foam_mm > 100:
            score -= 10

        # Vapour
        if self.app.vapour:
            score -= 10

        # Distance
        if self.app.distance_m > 20:
            score -= 20
        elif self.app.distance_m > 10:
            score -= 10

        # Antenna gain (added so optimizer can differentiate antennas)
        gains = {"ROD": 3, "HORN": 5, "LENS": 7}
        score += gains[self.antenna]

        return score

    def rating(self):
        score = self.suitability_score()
        if score >= 80:
            return score, "Excellent"
        elif score >= 60:
            return score, "Moderate"
        else:
            return score, "Challenging"

def recommend_frequency(app):
    if app.foam_mm > 300:
        return "26 GHz", "High foam → lower frequency preferred"
    elif app.dk < 2:
        return "26 GHz", "Low dielectric → stronger penetration at 26 GHz"
    elif app.distance_m > 20:
        return "26 GHz", "Long distance → lower frequency preferred"
    else:
        return "80 GHz", "Clean conditions → high resolution at 80 GHz"

class InterfaceDetectability:
    SPEED_OF_LIGHT = 299792458
    def __init__(self, oil_layer_cm, bandwidth_ghz=4):
        self.oil_layer_cm = oil_layer_cm
        self.bandwidth = bandwidth_ghz * 1e9
    def radar_resolution_cm(self):
        resolution_m = self.SPEED_OF_LIGHT / (2 * self.bandwidth)
        return resolution_m * 100
    def evaluate(self):
        resolution = self.radar_resolution_cm()
        if self.oil_layer_cm < resolution:
            return (False, resolution, "Interface may not be reliably distinguishable.")
        return (True, resolution, "Interface appears detectable.")

class ConfigOptimizer:
    def __init__(self, app):
        self.app = app
    def run(self):
        frequencies = [6, 26, 80]
        antennas = ["ROD", "HORN", "LENS"]
        results = {}
        for freq in frequencies:
            for ant in antennas:
                model = SignalBudget(self.app, freq, ant)
                results[(freq, ant)] = model.suitability_score()
        best = max(results, key=results.get)
        return results, best

class ReflectionCalculator:
    def __init__(self, er1, er2):
        self.er1 = er1
        self.er2 = er2
    def calculate(self):
        gamma = (math.sqrt(self.er2) - math.sqrt(self.er1)) / (math.sqrt(self.er2) + math.sqrt(self.er1))
        reflected_power = gamma**2 * 100
        echo_db = 10 * math.log10(gamma**2)
        return gamma, reflected_power, echo_db

class InstallationValidation:
    def __init__(self, antenna_od, nozzle_id, projection_mm, nozzle_height, beam_angle, blocking_mm, tank_height):
        self.antenna_od = antenna_od
        self.nozzle_id = nozzle_id
        self.projection_mm = projection_mm
        self.nozzle_height = nozzle_height
        self.beam_angle = beam_angle
        self.blocking_mm = blocking_mm
        self.tank_height = tank_height

    def check(self):
        results = []
        if self.antenna_od >= self.nozzle_id:
            results.append("❌ Antenna OD too large for nozzle ID.")
        else:
            results.append("✅ Nozzle clearance acceptable.")

        if self.projection_mm < self.nozzle_height:
            results.append("❌ Antenna projection too short, risk of false echoes.")
        else:
            results.append("✅ Antenna projection acceptable.")

        beam_diameter = 2 * (self.tank_height * (self.beam_angle/57.3))
        results.append(f"Beam diameter at liquid surface: {round(beam_diameter,2)} mm")
        if beam_diameter > self.nozzle_id:
            results.append("⚠️ Beam footprint may cause wall reflections.")
        else:
            results.append("✅ Beam footprint acceptable.")

        if self.blocking_mm > 300:
            results.append("⚠️ Blocking distance too large, near-surface blind zone.")
        else:
            results.append("✅ Blocking distance acceptable.")

        return results

class EngineeringBasis:
    def __init__(self, app, signal_margin):
        self.app = app
        self.signal_margin = signal_margin
    def generate(self):
        basis = []
        if self.app.dk < 2:
            basis.append(f"Low dielectric constant ({self.app.dk}) → weak reflections.")
        elif self.app.dk < 5:
            basis.append(f"Moderate dielectric constant ({self.app.dk}) → moderate reflections.")
        else:
            basis.append(f"High dielectric constant ({self.app.dk}) → strong reflections.")
        if self.app.foam_mm > 300:
            basis.append(f"High foam thickness ({self.app.foam_mm} mm) → strong attenuation.")
        elif self.app.foam_mm > 100:
            basis.append(f"Moderate foam thickness ({self.app.foam_mm} mm) → partial attenuation.")
        if self.app.vapour:
            basis.append("Process vapour present → additional attenuation.")
        if self.app.distance_m > 15:
            basis.append(f"Long measuring distance ({self.app.distance_m} m) → high path loss.")
        elif self.app.distance_m > 8:
            basis.append(f"Moderate measuring distance ({self.app.distance_m} m).")
        if self.signal_margin < 10:
            basis.append("Signal margin below recommended threshold.")
        elif self.signal_margin < 15:
            basis.append("Signal margin acceptable but limited.")
        else:
            basis.append("Signal margin healthy.")
        return basis

class CommentsGenerator:   # renamed from TBEGenerator
    def __init__(self, app, signal_margin, interface_ok):
        self.app = app
        self.signal_margin = signal_margin
        self.interface_ok = interface_ok
    def generate(self):
        comments = []
        if self.app.dk < 2:
            comments.append("Vendor to confirm performance in low dielectric hydrocarbon service.")
        if self.app.foam_mm > 300:
            comments.append("Vendor to confirm reliability in high foam conditions.")
        if self.signal_margin < 10:
            comments.append("Expected signal margin low. Provide project references.")
        if not self.interface_ok:
            comments.append("Vendor to confirm minimum detectable oil-water interface thickness.")
        comments.append("Provide references for similar slop tank installations.")
        return comments

# ============================================================
# STREAMLIT APP
# ============================================================
st.title("SMART NON-CONTACT RADAR LEVEL TRANSMITTER ENGINEERING ASSISTANT")

# Inputs
dk = st.number_input("Dielectric Constant", value=1.8)
foam_mm = st.number_input("Foam Thickness (mm)", value=500)
vapour = st.checkbox("Process Vapour Present?", value=True)
distance_m = st.number_input("Measuring Distance (m)", value=18)
oil_layer_cm = st.number_input("Oil Layer Thickness (cm)", value=2.0)

antenna_od = st.number_input("Antenna OD (mm)", value=80)
nozzle_id = st.number_input("Nozzle ID (mm)", value=100)
projection_mm = st.number_input("Antenna Projection Length (mm)", value=2000)
nozzle_height = st.number_input("Nozzle Height (mm)", value=150)
beam_angle = st.number_input("Beam Angle (deg)", value=2)
blocking_mm = st.number_input("Blocking Distance (mm)", value=300)
tank_height = st.number_input("Tank Height (mm)", value=2000)

if st.button("Run Analysis"):
    app = RadarApplication(dk, foam_mm, vapour, distance_m, oil_layer_cm)

    # 1. Application Assessment
    st.header("1. Application Assessment")
    st.write(f"Dielectric Constant: {dk}")
    st.write(f"Foam Thickness: {foam_mm} mm")
    st.write(f"Measuring Distance: {distance_m} m")
    st.write(f"Oil Layer Thickness: {oil_layer_cm} cm")

    
        # Reflected Power Calculation
    st.subheader("Reflected Power at Product Surface")
    gamma, power, echo_db = ReflectionCalculator(1.0, dk).calculate()
    st.write(f"Reflection Coefficient Γ: {round(gamma,3)}")
    st.write(f"Reflected Power: {round(power,2)} %")
    st.write(f"Echo Level: {round(echo_db,2)} dB below perfect reflector")

    # 2. Technology Selection
    st.header("2. Technology Selection")

    config_results, best_config = ConfigOptimizer(app).run()
    for (freq, ant), val in config_results.items():
        st.write(f"{freq} GHz + {ant} : {val} (Suitability Score)")

    # Tie-breaker logic
    scores = list(config_results.values())
    if len(set(scores)) == 1:  # all scores equal
        best_freq, reason = recommend_frequency(app)
        st.success(f"Recommended Frequency (Engineering Rule): {best_freq} → {reason}")
        best_ant = None  # no antenna chosen when tied
    else:
        best_freq, best_ant = best_config
        st.success(f"Recommended Configuration: {best_freq} GHz + {best_ant}")

    # Final Suitability Rating
    final_model = SignalBudget(app, best_freq, best_ant if best_ant else "ROD")
    score, rating = final_model.rating()

    st.subheader("Engineering Suitability Index")
    st.write(f"Score: {score}, Rating: {rating}")

    # Frequency recommendation based on engineering rules
    freq_choice, freq_reason = recommend_frequency(app)
    st.info(f"Recommended Frequency (Engineering Rule): {freq_choice} → {freq_reason}")

    # Frequency explanation
    if best_freq == 6:
        freq_reason = "6 GHz suffers the least attenuation from foam, vapour, and long distance."
    elif best_freq == 26:
        freq_reason = "26 GHz balances attenuation and resolution, suitable for moderate conditions."
    else:
        freq_reason = "80 GHz provides high resolution but suffers more attenuation, best for clean conditions."
    st.info(f"Why {best_freq} GHz? {freq_reason}")

    # Antenna explanation
    if best_ant:
        if best_ant == "LENS":
            ant_reason = "LENS antenna has the highest gain (+7 dB), giving the strongest signal margin."
        elif best_ant == "HORN":
            ant_reason = "HORN antenna provides focused energy, useful for moderate DK and vapour conditions."
        else:
            ant_reason = "ROD antenna is compact but lower gain, suitable for simple applications."
        st.info(f"Why {best_ant}? {ant_reason}")
    else:
        st.info("Antenna selection depends on installation constraints (no single best choice).")

    # Risk Assessment (based on Suitability Score)
    if score >= 80:
        risk = "LOW"
    elif score >= 60:
        risk = "MEDIUM"
    else:
        risk = "HIGH"

    # Interface Detectability
    interface = InterfaceDetectability(app.oil_layer_cm)
    interface_ok, resolution, msg = interface.evaluate()

    # 3. Installation Validation
    st.header("3. Installation Validation")
    validation = InstallationValidation(
        antenna_od, nozzle_id, projection_mm, nozzle_height,
        beam_angle, blocking_mm, tank_height
    ).check()
    for item in validation:
        st.markdown(f"- {item}")

    # 4. Engineering Review
    st.header("4. Engineering Review")

    # Measurement Risk
    st.subheader("Measurement Risk")
    if risk == "HIGH":
        st.error(f"🚨 HIGH RISK - Suitability Score {score}, Rating: {rating}")
    elif risk == "MEDIUM":
        st.warning(f"⚠️ MEDIUM RISK - Suitability Score {score}, Rating: {rating}")
    else:
        st.success(f"✅ LOW RISK - Suitability Score {score}, Rating: {rating}")

    # Interface Detectability
    st.subheader("Interface Detectability")
    st.write(f"Oil Layer: {app.oil_layer_cm} cm")
    st.write(f"Radar Resolution: {round(resolution,2)} cm")
    st.write(msg)

    # Engineering Basis
    st.subheader("Engineering Basis")
    basis = EngineeringBasis(app, score).generate()
    for item in basis:
        st.markdown(f"- {item}")

    # Comments (renamed from TBE Comments)
    st.subheader("Comments")
    comments = CommentsGenerator(app, score, interface_ok).generate()
    for comment in comments:
        st.markdown(f"- {comment}")

    # Final Recommendation
    st.subheader("Final Engineering Recommendation")
    if risk == "HIGH":
        st.error("🚨 REVIEW REQUIRED - Application appears challenging. Vendor confirmation essential.")
    elif risk == "MEDIUM":
        st.warning("⚠️ CONDITIONAL ACCEPTANCE - Vendor confirmation recommended before approval.")
    else:
        st.success("✅ APPLICATION ACCEPTABLE - Ready for implementation.")
