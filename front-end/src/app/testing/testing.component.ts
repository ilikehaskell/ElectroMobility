import { Component, OnInit } from '@angular/core';
import { Socket } from 'ng-socket-io';

@Component({
  selector: 'app-testing',
  templateUrl: './testing.component.html',
  styleUrls: ['./testing.component.css']
})
export class TestingComponent implements OnInit {

  constructor(private socket: Socket) { }

  ngOnInit() {
  }

  writeSocket(message) {
    this.socket.write('move', message);
  }

}
