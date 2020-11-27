import { ɵSWITCH_COMPILE_COMPONENT__POST_R3__ } from '@angular/core';

export class Controller {
  public buttons: number[] = new Array(16);
  public axes: number[] = new Array(4);
  public timestamp: number;
  private pre6: number = 0.5;
  private pre7: number = 0.5;

  constructor(controller: Gamepad) {
    this.writeController;
  }

  writeController(controller: Gamepad) {
    this.timestamp = controller.timestamp;

    if (controller.axes.length === 8) {
      this.ps4ToStandard(controller);
    } else if (controller.axes.length === 6) {
      this.oldPSToStandard(controller);
    } else if (
      controller.axes.length === 4 ||
      controller.mapping === 'standard'
    ) {
      this.commonToStandard(controller);
    } else {
      console.log('This controller does not seem to be supported.');
    }
  }

  updateController(controller: Gamepad) {
    this.timestamp = controller.timestamp;

    this.writeController(controller);
  }

  ps4ToStandard(controller: Gamepad) {
    if (this.pre6 && controller.axes[2] != 0) {
      this.pre6 = 0;
    }

    if (this.pre7 && controller.axes[5] != 0) {
      this.pre7 = 0;
    }

    this.buttons[0] = controller.buttons[0].value;
    this.buttons[1] = controller.buttons[1].value;
    this.buttons[2] = controller.buttons[3].value;
    this.buttons[3] = controller.buttons[2].value;
    this.buttons[4] = controller.buttons[4].value;
    this.buttons[5] = controller.buttons[5].value;
    this.buttons[6] =
      (controller.axes[2].valueOf() + 1) / 2 - this.pre6 > 0.15 ? 1 : 0;
    this.buttons[7] =
      (controller.axes[5].valueOf() + 1) / 2 - this.pre7 > 0.15 ? 1 : 0;
    if (controller.buttons.length > 12) {
      this.buttons[8] = controller.buttons[8].value;
      this.buttons[9] = controller.buttons[9].value;
      this.buttons[10] = controller.buttons[11].value;
      this.buttons[11] = controller.buttons[12].value;
      this.buttons[16] = controller.buttons[10].value;
    } else {
      this.buttons[8] = controller.buttons[6].value;
      this.buttons[9] = controller.buttons[7].value;
      this.buttons[10] = controller.buttons[9].value;
      this.buttons[11] = controller.buttons[10].value;
      this.buttons[16] = controller.buttons[8].value;
    }
    this.buttons[12] = controller.axes[7].valueOf() <= -0.15 ? 1 : 0;
    this.buttons[13] = controller.axes[7].valueOf() >= 0.15 ? 1 : 0;
    this.buttons[14] = controller.axes[6].valueOf() <= -0.15 ? 1 : 0;
    this.buttons[15] = controller.axes[6].valueOf() >= 0.15 ? 1 : 0;

    let i = 0;

    for (let j = 0; j < this.axes.length; j++) {
      let input = controller.axes[i].valueOf();
      if (input <= -0.15) {
        this.axes[j] = -1;
      } else if (input >= 0.15) {
        this.axes[j] = 1;
      } else {
        this.axes[j] = 0;
      }

      i = i === 1 ? i + 2 : i + 1;
    }
  }

  oldPSToStandard(controller: Gamepad) {
    if (this.pre6 && controller.axes[2] != 0) {
      this.pre6 = 0;
    }

    if (this.pre7 && controller.axes[5] != 0) {
      this.pre7 = 0;
    }

    this.buttons[0] = controller.buttons[0].value;
    this.buttons[1] = controller.buttons[1].value;
    this.buttons[2] = controller.buttons[3].value;
    this.buttons[3] = controller.buttons[2].value;
    this.buttons[4] = controller.buttons[4].value;
    this.buttons[5] = controller.buttons[5].value;
    this.buttons[6] =
      (controller.axes[2].valueOf() + 1) / 2 - this.pre6 >
      controller.axes[1].valueOf() + 1
        ? 1
        : 0;
    this.buttons[7] =
      (controller.axes[5].valueOf() + 1) / 2 - this.pre7 >
      controller.axes[1].valueOf() + 1
        ? 1
        : 0;
    this.buttons[8] = controller.buttons[8].value;
    this.buttons[9] = controller.buttons[9].value;
    this.buttons[10] = controller.buttons[11].value;
    this.buttons[11] = controller.buttons[12].value;
    this.buttons[12] = controller.buttons[13].value;
    this.buttons[13] = controller.buttons[14].value;
    this.buttons[14] = controller.buttons[15].value;
    this.buttons[15] = controller.buttons[16].value;
    this.buttons[16] = controller.buttons[10].value;

    let i = 0;

    for (let j = 0; j < this.axes.length; j++) {
      let input = controller.axes[i].valueOf();
      if (input <= -0.15) {
        this.axes[j] = -1;
      } else if (input >= 0.15) {
        this.axes[j] = 1;
      } else {
        this.axes[j] = 0;
      }

      i = i === 1 ? i + 2 : i + 1;
    }
  }

  commonToStandard(controller: Gamepad) {
    for (let i: number = 0; i < 17; i++) {
      this.buttons[i] = controller.buttons[i].value;
    }

    for (let i: number = 0; i < 4; i++) {
      const input = controller.axes[i].valueOf();
      if (input <= -0.15) {
        this.axes[i] = -1;
      } else if (input >= 0.15) {
        this.axes[i] = 1;
      } else {
        this.axes[i] = 0;
      }
    }
  }
}
