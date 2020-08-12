import { Component, OnInit, Input } from '@angular/core';
import { Run, numHash } from '../interfaces';
import { RunService } from '../run.service';

@Component({
  selector: 'app-list',
  templateUrl: './list.component.html',
  styleUrls: ['./list.component.css']
})

export class ListComponent implements OnInit {

  runs: Run[];
  tagBoxes: numHash;
  @Input() runType: number;

  constructor(
    private runService: RunService
  ) { }

  ngOnInit(): void {
    this.getRuns();
  }

  toggleTags(target) {
    target = !target;
  }

  makeTagVar(target) {
    this.tagBoxes[target] = false;
    console.log("targ making :" + target + ", " + this.tagBoxes[target]);
  }

  getRuns() {
    this.runService.getRuns(this.runType)
      .subscribe(runs => this.runs = runs)
    console.log("list of runs: ");
    this.runs.forEach(element => {
      console.log(element.name);
    });
  }
}
