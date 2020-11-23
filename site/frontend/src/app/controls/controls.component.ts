import { Component, HostListener, OnInit } from '@angular/core';
import { Socket } from 'ngx-socket-io';
import { StreamService } from '../stream.service';
import { Controller } from '../classes';

@Component({
  selector: 'app-controls',
  templateUrl: './controls.component.html',
  styleUrls: ['./controls.component.css'],
})
export class ControlsComponent implements OnInit {
  @HostListener('document:keydown', ['$event'])
  handleKeyboardPress(event: KeyboardEvent) {
    if (!event.repeat) {
      const action: String = this.keyboardEnum[event.key];
      if (action && !this.commandState.has(action.toLocaleLowerCase())) {
        try {
          this.commandState.set(action, true);
          if (action.includes('cam')) {
            this.onCamClickD(action);
          } else if (action === 'speedUp') {
            if (this.slider <= 95) {
              this.slider += 5;
            }
          } else if (action === 'speedDown') {
            if (this.slider >= 5) {
              this.slider -= 5;
            }
          } else if (action === 'binary') {
            this.onBinClick('True');
          } else if (action === 'eBrake') {
            this.socketEmit('eBrake');
          } else if (action === 'capture') {
            this.caputerImage();
          } else {
            this.onClickD(action);
          }
        } catch {
          console.log("doesn't exist");
        }
      }
    }
  }

  @HostListener('document:keyup', ['$event'])
  handleKeyboardlift(event: KeyboardEvent) {
    try {
      const action: String = this.keyboardEnum[event.key];
      this.commandState.delete(action);

      if (action.includes('cam')) {
        this.onCamClickR(action);
      } else if (action === 'binary') {
        this.onBinClick('False');
      } else if (
        action.includes('speed') ||
        action === 'capture' ||
        action === 'eBrake'
      ) {
        return;
      } else if (action) {
        this.onClickR(action);
      }
    } catch {
      console.log("doesn't exist");
    }
  }

  @HostListener('window:gamepadconnected', ['$event'])
  handleControllerConnect(event) {
    this.addGamepad(event.gamepad);
    if (!this.intervalRunning) {
      this.gamepadInterval = setInterval(() => {
        this.updateStatus();
      }, 100);
    }
  }

  @HostListener('window:gamepaddisconnected', ['$event'])
  handleControllerDisconnected(event) {
    this.removeGamepad(event);
    if (this.gamepads.every((item) => item === null)) {
      clearInterval(this.gamepadInterval);
    }
    console.log('Gamepad disconnected');
  }

  commandState = new Map();

  gamepadInterval;
  intervalRunning: boolean = false;
  gamepads: Gamepad[] = [];
  controllers: Controller[] = [];
  prevControllers: Controller[] = [];
  slider: number = 50;

  constructor(private socket: Socket, private streamService: StreamService) {}

  ngOnInit(): void {
    // get speed from python
  }

  setSingleMovement(target: String, value: boolean) {
    this.commandState.set(target, value);
  }

  onClickD(button) {
    if (button === 'left') {
      this.socketEmit('movement', 'turn', (this.slider / 100) * -1);
    } else if (button === 'right') {
      this.socketEmit('movement', 'turn', this.slider / 100);
    } else if (button === 'back') {
      this.socketEmit('movement', 'straight', (this.slider / 100) * -1);
    } else {
      this.socketEmit('movement', 'straight', this.slider / 100);
    }
  }

  onClickR(button) {
    if (button === 'left' || button === 'right') {
      this.socketEmit('stopMotors', 'turn');
    } else {
      this.socketEmit('stopMotors', 'straight');
    }
  }

  onCamClickD(button) {
    if (button === 'camLeft') {
      this.socketEmit('camera', 'x', 1);
    } else if (button === 'camRight') {
      this.socketEmit('camera', 'x', -1);
    } else if (button === 'camDown') {
      this.socketEmit('camera', 'y', -1);
    } else {
      this.socketEmit('camera', 'y', 1);
    }
  }

  onCamClickR(button) {
    if (button === 'camLeft' || button === 'camRight') {
      this.socketEmit('stopCam', 'x');
    } else {
      this.socketEmit('stopCam', 'y');
    }
  }

  onBinClick(state) {
    this.socketEmit('binary', state);
  }

  caputerImage() {
    this.streamService.captureImage();
  }

  addGamepad(gamepad: Gamepad) {
    console.log('Gamepad connected');
    try {
      this.gamepads[gamepad.index] = gamepad;
      this.controllers[gamepad.index] = new Controller(gamepad);
      this.prevControllers[gamepad.index] = new Controller(gamepad);
    } catch {
      this.gamepads.push(gamepad);
      this.controllers.push(new Controller(gamepad));
      this.prevControllers.push(new Controller(gamepad));
    }
  }

  removeGamepad(gamepad: Gamepad) {
    this.gamepads.splice(gamepad.index, 1, null);
    this.controllers.splice(gamepad.index, 1, null);
    this.prevControllers.splice(gamepad.index, 1, null);
  }

  updateStatus() {
    if (this.intervalRunning) {
      this.scanGamepads();
    }

    this.gamepads.forEach((gamepad: Gamepad, index) => {
      if (!this.controllers[index]) {
        this.controllers.push(new Controller(gamepad));
        return;
      } else if (gamepad.timestamp === this.controllers[index].timestamp) {
        return;
      } else {
        this.controllers[index].updateController(gamepad);
      }

      if (this.controllers[index].buttons[5] > 0) {
        if (
          this.controllers[index].buttons[5] !==
          this.prevControllers[index].buttons[5]
        ) {
          this.socketEmit('stop');
        }
        this.prevControllers[index].updateController(gamepad);
        return;
      }

      if (this.controllers[index].buttons[6] > 0) {
        if (
          this.controllers[index].buttons[6] !==
          this.prevControllers[index].buttons[6]
        ) {
          this.socketEmit('camHolt');
        }
        this.prevControllers[index].updateController(gamepad);
        return;
      }

      if (
        this.controllers[index].buttons[4] !==
          this.prevControllers[index].buttons[4] &&
        this.controllers[index].buttons[4]
      ) {
        this.streamService.captureImage();
      }

      if (
        this.controllers[index].buttons[11] !==
          this.prevControllers[index].buttons[11] &&
        this.controllers[index].buttons[11]
      ) {
        this.streamService.refocus();
      }

      if (
        this.controllers[index].buttons[7] !==
          this.prevControllers[index].buttons[7] &&
        this.controllers[index].buttons[7]
      ) {
        this.socketEmit('binary', 'True');
      } else if (
        this.controllers[index].buttons[7] !==
        this.prevControllers[index].buttons[7]
      ) {
        this.socketEmit('binary', 'False');
      }

      let movementChange: boolean = false;

      for (let i: number = 12; i <= 15; i++) {
        if (
          this.controllers[index].buttons[i] !=
          this.prevControllers[index].buttons[i]
        ) {
          movementChange = true;
        }
      }

      if (movementChange) {
        for (let i: number = 12; i <= 15; i++) {
          if (
            this.controllers[index].buttons[i] &&
            this.controllers[index].buttons[i] !=
              this.prevControllers[index].buttons[i]
          ) {
            switch (i) {
              case 12: {
                this.socketEmit('movement', 'straight', this.slider / 100);
                break;
              }
              case 13: {
                this.socketEmit(
                  'movement',
                  'straight',
                  (this.slider / 100) * -1
                );
                break;
              }
              case 14: {
                this.socketEmit('movement', 'turn', (this.slider / 100) * -1);
                break;
              }
              case 15: {
                this.socketEmit('movement', 'turn', this.slider / 100);
                break;
              }
              default: {
                console.log('something failed!');
                break;
              }
            }

            break;
          } else {
            if (i < 14) {
              this.socketEmit('stopMotors', 'straight');
            } else {
              this.socketEmit('stopMotors', 'turn');
            }
          }
        }
      }

      if (
        this.controllers[index].axes[2] !== this.prevControllers[index].axes[2]
      ) {
        if (this.controllers[index].axes[2]) {
          this.socketEmit('camera', 'x', this.controllers[index].axes[2] * -1);
        } else {
          this.socketEmit('stopCam', 'x');
        }
      }

      if (
        this.controllers[index].axes[3] !== this.prevControllers[index].axes[3]
      ) {
        if (this.controllers[index].axes[3]) {
          this.socketEmit('camera', 'y', this.controllers[index].axes[3] * -1);
        } else {
          this.socketEmit('stopCam', 'y');
        }
      }
      this.prevControllers[index].updateController(gamepad);
    });
  }

  scanGamepads() {
    let gamepads: Gamepad[] = navigator.getGamepads
      ? navigator.getGamepads()
      : [];

    gamepads.forEach((gamepad: Gamepad) => {
      if (gamepad) {
        if (this.gamepads[gamepad.index]) {
          this.gamepads[gamepad.index] = gamepad;
        } else {
          this.addGamepad(gamepad);
        }
      }
    });
  }

  socketEmit(channel: string, command?: string, args?: Number | String) {
    if (channel === 'stop') {
      this.socket.emit(channel);
    } else if (channel === 'stopMotors') {
      this.socket.emit(channel, command);
    } else if (channel === 'binary') {
      this.socket.emit(channel, command);
    } else if (channel === 'stopCam') {
      this.socket.emit(channel, command);
      console.log('stopCam');
    } else if (channel === 'speed') {
      this.socket.emit(channel, this.slider / 100); //does it really need this info
    } else if (command) {
      const speed = args || args <= 0 ? args : 1;
      this.socket.emit(channel, command, speed);
    } else {
      this.socket.emit(channel);
    }
  }
  refocus() {
    this.streamService.refocus();
  }

  private keyboardEnum = Object.freeze({
    w: 'forward',
    a: 'left',
    d: 'right',
    s: 'back',
    ArrowUp: 'camUp',
    ArrowLeft: 'camLeft',
    ArrowRight: 'camRight',
    ArrowDown: 'camDown',
    q: 'binary',
    e: 'capture',
    r: 'speedUp',
    f: 'speedDown',
    ' ': 'eBrake',
  });
}
