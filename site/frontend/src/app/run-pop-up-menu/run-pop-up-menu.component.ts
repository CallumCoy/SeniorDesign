import { Component, Injectable, OnInit } from '@angular/core';
import { ToggleService } from '../toggle.service';

import { Run } from '../interfaces';
import { RunService } from '../run.service';
import { StreamService } from '../stream.service';

@Injectable({
  providedIn: 'root',
})
@Component({
  selector: 'app-run-pop-up-menu',
  templateUrl: './run-pop-up-menu.component.html',
  styleUrls: ['./run-pop-up-menu.component.css'],
})
export class RunPopUpMenuComponent implements OnInit {
  newRun: Run;
  temp: Run;
  hideHTML: boolean;

  constructor(
    private runService: RunService,
    private toggleService: ToggleService,
    private streamService: StreamService
  ) {}

  ngOnInit(): void {
    this.toggleService.getHideNew().subscribe((value) => {
      this.hideHTML = value;
    });
    this.runService.getNewRun().subscribe((value) => {
      this.newRun = value;
    });
    this.temp = this.runService.createEmptyRun();
  }

  comfirmBut(
    name,
    driverName,
    pipeID,
    dir,
    lat,
    latM,
    latS,
    latType,
    long,
    longM,
    longS,
    longType,
    record
  ) {
    this.temp.Name = name;
    this.temp.DriverName = driverName;
    this.temp.PipeID = pipeID;
    this.temp.Direction = dir;
    this.temp.Lat = this.todegrees(Number(lat), latM, latS, Number(latType));
    this.temp.Longi = this.todegrees(
      Number(long),
      longM,
      longS,
      Number(longType)
    );
    this.temp.Tagged = 0;

    this.streamService.run(dir, this.temp.Lat, this.temp.Longi, record);

    this.runService.setNewRun(this.temp);

    this.toggleService.operateNewWindow();
  }

  cancelBut() {
    this.toggleService.setButtonOp('New Run');
    this.toggleService.toggleHideNew();
  }

  todegrees(baseDeg, minutes?, seconds?, sign?) {
    const degMinutes = (minutes || 0) / 60;
    const degSeconds = (seconds || 0) / 3600;
    const degSign = sign || 0;

    if (degSign > 0) {
      return Math.abs(baseDeg) + degMinutes + degSeconds;
    } else if (degSign === 0) {
      if (baseDeg != 0) {
        return (
          baseDeg +
          degMinutes * (baseDeg / Math.abs(baseDeg)) +
          degSeconds * (baseDeg / Math.abs(baseDeg))
        );
      } else {
        return baseDeg + degMinutes + degSeconds;
      }
    } else {
      return Math.abs(baseDeg) * -1 - degMinutes - degSeconds;
    }
  }
}
