from kitty_move import move_legs, pca, set_leg_offset, save_offsets, load_offsets
from time import sleep
import sys
import termios
import tty


def get_key():
    """Read a single keypress from the terminal."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        key = sys.stdin.read(1)
        # Handle arrow keys (they send 3 characters)
        if key == '\x1b':
            key += sys.stdin.read(2)
        return key
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def calibrate_legs():
    """
    Calibrate each joint by adjusting angles until they're at true 90 degrees.

    Use arrow keys to adjust:
    - Left arrow: decrease angle
    - Right arrow: increase angle
    - Enter: confirm and move to next joint
    - 'q': quit calibration
    """
    # Define all joints to calibrate
    joints = [
        ('fl', 'top', 'Front Left - Top Joint (Hip)'),
        ('fl', 'bottom', 'Front Left - Bottom Joint (Knee)'),
        ('fr', 'top', 'Front Right - Top Joint (Hip)'),
        ('fr', 'bottom', 'Front Right - Bottom Joint (Knee)'),
        ('bl', 'top', 'Back Left - Top Joint (Hip)'),
        ('bl', 'bottom', 'Back Left - Bottom Joint (Knee)'),
        ('br', 'top', 'Back Right - Top Joint (Hip)'),
        ('br', 'bottom', 'Back Right - Bottom Joint (Knee)'),
    ]

    # Store offsets as we calibrate
    offsets = {}

    print("=" * 60)
    print("CALIBRATION MODE")
    print("=" * 60)
    print("\nInstructions:")
    print("  - Use LEFT/RIGHT arrow keys to adjust the joint")
    print("  - Adjust until the joint is at TRUE 90 degrees")
    print("  - Press ENTER to confirm and move to next joint")
    print("  - Press 'q' to quit\n")

    for leg, joint_type, description in joints:
        current_angle = 90

        print(f"\n{description}")
        print(f"Starting at 90 degrees. Adjust as needed...")

        # Set initial position
        if joint_type == 'top':
            move_legs(leg, current_angle, 90)
        else:
            move_legs(leg, 90, current_angle)

        while True:
            print(f"  Current angle: {current_angle}° (offset: {current_angle - 90:+d}°)", end='\r')

            key = get_key()

            # Left arrow: decrease
            if key == '\x1b[D':
                current_angle = max(0, current_angle - 1)
                if joint_type == 'top':
                    move_legs(leg, current_angle, 90)
                else:
                    move_legs(leg, 90, current_angle)

            # Right arrow: increase
            elif key == '\x1b[C':
                current_angle = min(180, current_angle + 1)
                if joint_type == 'top':
                    move_legs(leg, current_angle, 90)
                else:
                    move_legs(leg, 90, current_angle)

            # Enter: confirm
            elif key == '\n' or key == '\r':
                offset = current_angle - 90
                offsets[f"{leg}_{joint_type}"] = offset
                print(f"\n  ✓ Confirmed! Offset: {offset:+d}°")
                break

            # Quit
            elif key == 'q' or key == 'Q':
                print("\n\nCalibration cancelled.")
                return

        sleep(0.3)

    # Save all offsets
    print("\n" + "=" * 60)
    print("Calibration complete! Saving offsets...")

    for joint_name, offset in offsets.items():
        leg, joint_type = joint_name.split('_')
        set_leg_offset(leg, joint_type, offset)

    save_offsets()
    print("Offsets saved to calibration.json")
    print("=" * 60)

    # Return to neutral
    move_legs('all', 90, 90)


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
    # Load calibration offsets
    load_offsets()

    print("Robot Control Menu:")
    print("1. Calibrate legs")
    print("2. Walk forward")
    print("3. Exit")

    choice = input("\nEnter choice (1-3): ").strip()

    if choice == '1':
        calibrate_legs()
    elif choice == '2':
        walk_forward(steps=2, step_duration=0.3)
    else:
        print("Exiting...")

    # Clean up
    pca.deinit()
