# coding: utf-8

import sys
import cozmo
from cozmo.util import degrees
from slackbot.bot import default_reply
from slackbot.bot import respond_to
from slackbot.bot import listen_to

def extract_float(val):
    try:
        float_val = float(val)
        return float_val
    except ValueError:
        pass

# Slackからコマンド以外のものはCozmoが喋る
@default_reply()
def default_func(message):
    global msg
    msg = message.body['text'] # メッセージを取り出す
    cozmo.run_program(cozmo_say)

@respond_to(r'^say (.*)')
@listen_to(r'^say (.*)')
def cozmo_say(message, args):
    global msg
    msg = args
    cozmo.run_program(cozmo_say)

# Cozmoに喋らせる
def cozmo_say(robot: cozmo.robot.Robot):
    if (msg is not None) and (len(msg) > 0):
        robot.say_text(msg).wait_for_completed()

# Cozmoの移動
@respond_to(r'^drive (.*)')
@listen_to(r'^drive (.*)')
def cozmo_drive(message, args):
    global duration
    duration = args
    cozmo.run_program(do_drive)

def do_drive(robot: cozmo.robot.Robot):
    drive_duration = extract_float(duration)
    if drive_duration is not None:
        drive_speed = 50
        drive_dir = "forwards"
        if drive_duration < 0:
            drive_speed = -drive_speed
            drive_duration = -drive_duration
            drive_dir = "backwards"
        robot.drive_wheels(drive_speed, drive_speed, duration=drive_duration)

@respond_to(r'^turn (.*)')
@listen_to(r'^turn (.*)')
def cozmo_turn(message, args):
    global turn
    turn = args
    cozmo.run_program(do_turn)

def do_turn(robot: cozmo.robot.Robot):
    drive_angle = extract_float(turn)

    if drive_angle is not None:
        robot.turn_in_place(degrees(drive_angle)).wait_for_completed()

@respond_to(r'^lift (.*)')
@listen_to(r'^lift (.*)')
def cozmo_lift(message, args):
    global lift
    lift = args
    cozmo.run_program(do_lift)

def do_lift(robot: cozmo.robot.Robot):
    lift_height = extract_float(lift)

    if lift_height is not None:
        robot.set_lift_height(height=lift_height).wait_for_completed()

@respond_to(r'^head (.*)')
@listen_to(r'^head (.*)')
def cozmo_head(message, args):
    global head
    head = args
    cozmo.run_program(do_head)

def do_head(robot: cozmo.robot.Robot):
        head_angle = extract_float(head)

        if head_angle is not None:
            head_angle_action = robot.set_head_angle(degrees(head_angle))
            clamped_head_angle = head_angle_action.angle.degrees
            head_angle_action.wait_for_completed()
