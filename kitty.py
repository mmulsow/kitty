from kitty_move import move_legs, pca
from time import sleep


def walk_forward(steps=4, step_duration=0.3):
    """
    Make the robot walk forward using a crawl gait.

    Gait sequence: FL -> BR -> FR -> BL (diagonal pattern for stability)

    Args:
        steps: Number of complete walking cycles
        step_duration: Time for each phase of leg movement (seconds)
    """
    # Base stance angles
    stance_top = 90
    stance_bottom = 90

    # Movement parameters
    lift_bottom = 60      # Knee bend to lift leg
    swing_forward = 110   # Hip swing forward
    swing_back = 70       # Hip swing back for support legs

    print(f"Walking forward for {steps} steps...")

    # Start in neutral stance
    move_legs('all', stance_top, stance_bottom)
    sleep(0.5)

    for step in range(steps):
        print(f"Step {step + 1}/{steps}")

        # 1. Move Front Left leg
        move_legs('fl', stance_top, lift_bottom)  # Lift
        sleep(step_duration)
        move_legs('fl', swing_forward, lift_bottom)  # Swing forward
        sleep(step_duration)
        move_legs('fl', swing_forward, stance_bottom)  # Place down
        move_legs('fr', swing_back, stance_bottom)  # Push with other legs
        move_legs('bl', swing_back, stance_bottom)
        move_legs('br', swing_back, stance_bottom)
        sleep(step_duration)

        # 2. Move Back Right leg
        move_legs('br', stance_top, lift_bottom)  # Lift
        sleep(step_duration)
        move_legs('br', swing_forward, lift_bottom)  # Swing forward
        sleep(step_duration)
        move_legs('br', swing_forward, stance_bottom)  # Place down
        move_legs('fl', swing_back, stance_bottom)  # Push with other legs
        move_legs('fr', swing_back, stance_bottom)
        move_legs('bl', swing_back, stance_bottom)
        sleep(step_duration)

        # 3. Move Front Right leg
        move_legs('fr', stance_top, lift_bottom)  # Lift
        sleep(step_duration)
        move_legs('fr', swing_forward, lift_bottom)  # Swing forward
        sleep(step_duration)
        move_legs('fr', swing_forward, stance_bottom)  # Place down
        move_legs('fl', swing_back, stance_bottom)  # Push with other legs
        move_legs('bl', swing_back, stance_bottom)
        move_legs('br', swing_back, stance_bottom)
        sleep(step_duration)

        # 4. Move Back Left leg
        move_legs('bl', stance_top, lift_bottom)  # Lift
        sleep(step_duration)
        move_legs('bl', swing_forward, lift_bottom)  # Swing forward
        sleep(step_duration)
        move_legs('bl', swing_forward, stance_bottom)  # Place down
        move_legs('fl', swing_back, stance_bottom)  # Push with other legs
        move_legs('fr', swing_back, stance_bottom)
        move_legs('br', swing_back, stance_bottom)
        sleep(step_duration)

    # Return to neutral stance
    print("Returning to neutral stance...")
    move_legs('all', stance_top, stance_bottom)
    sleep(0.5)
    print("Walk complete!")


if __name__ == "__main__":
    # Test the walking function
    walk_forward(steps=2, step_duration=0.3)

    # Clean up
    pca.deinit()
