import { Component, ViewChild, HostListener } from '@angular/core';
import { VideoService, loadBinaryResource } from './video.service';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
})
export class AppComponent {
  @ViewChild('videoElement') videoElement: any;
  video: any;
  isShown: boolean = false;
  sideList: boolean = true;
  pullOutBar: boolean = true;
  title = 'site';
  operation = 'New Run';
  pullOutCont = '<===';
  innerWidth: any;
  primaryCam;

  constructor(private videoService: VideoService) {}

  ngOnInit() {
    this.primaryCam = this.getVideo;
    this.innerWidth = window.innerWidth;

    if (this.innerWidth < 1775) {
      this.sideList = false;
      this.pullOutBar = true;
    } else {
      this.sideList = true;
      this.pullOutBar = false;
    }
  }

  @HostListener('window:resize', ['$event'])
  onResize(event) {
    this.innerWidth = window.innerWidth;

    if (this.innerWidth < 1775 && !this.pullOutBar) {
      this.pullOutBar = true;
    } else if (this.innerWidth >= 1775 && this.pullOutBar) {
      this.pullOutBar = false;
    }

    if (this.innerWidth < 1775 && this.sideList) {
      this.sideList = false;
    } else if (this.innerWidth >= 1775 && !this.sideList) {
      this.sideList = true;
    }
  }

  toggleOption() {
    if (this.operation === 'New Run') {
      this.toggleShow();
      this.operation = '';
    } else if (this.operation === '') {
      this.toggleShow();
      this.operation = 'End Run';
    } else {
      this.operation = 'New Run';
      //TODO send data to server
    }
  }

  toggleSideMenu() {
    this.sideList = !this.sideList;

    if (this.pullOutCont === '<===') {
      this.pullOutCont = 'X';
    } else {
      this.pullOutCont = '<===';
    }
  }

  toggleShow() {
    this.isShown = !this.isShown;
  }

  fillData(runID) {
    if (runID === null) {
      return;
    } else if (runID === 'newRun') {
    }
  }

  getVideo(): Observable<any> {
    return <any>loadBinaryResource();
  }
}
