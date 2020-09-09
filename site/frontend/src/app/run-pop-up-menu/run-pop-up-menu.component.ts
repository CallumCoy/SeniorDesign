import { Component, OnInit } from '@angular/core';
import { AppComponent } from '../app.component';

import { Run } from '../interfaces';
import { RunService } from '../run.service';

@Component({
  selector: 'app-run-pop-up-menu',
  templateUrl: './run-pop-up-menu.component.html',
  styleUrls: ['./run-pop-up-menu.component.css'],
})
export class RunPopUpMenuComponent implements OnInit {
  run: Run;

  constructor(private app: AppComponent, private runService: RunService) {}

  ngOnInit(): void {
    this.getRun();
  }

  getRun() {
    this.runService
      .getRun(-1) // How to make it so -1's data is remembered
      .subscribe((run) => (this.run = run));
  }

  toggleShow() {
    this.app.operation = 'New Run';
    this.app.toggleShow();
  }

  newRun() {
    this.run.Id = -1;
    this.run.Date = new Date();
    //this.runService.addRun(this.run);
  }
}
