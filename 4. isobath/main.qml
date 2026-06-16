import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtWebEngine 1.10
import QtWebChannel 1.15

Window {
    width: 1024
    height: 768
    visible: true
    title: "3D CLMS"
    color : "#012340"

    property var line_color : "#03A678"

    Text {
        anchors.horizontalCenter: parent.horizontalCenter
        x: 0
        y: 0
        color: "#ffffff"
        text: "PyQt5 benchmark 3D"
        font.pixelSize: 22
        font.styleName: "Bold"
        font.weight: Font.Bold

        Text {
            anchors.horizontalCenter: parent.horizontalCenter
            x: 0
            y: 30
            color: line_color
            text: "WRITTEN BY : MUHAMMAD HUSNI MUTTAQIN"
            font.pixelSize: 18
            font.styleName: "Bold"
            font.weight: Font.Bold
        }
    }

    Rectangle {
        width  : parent.width  * 0.8
        height : parent.height * 0.8
        border.color : line_color
        border.width : 4
        anchors.verticalCenter:   parent.verticalCenter
        anchors.horizontalCenter: parent.horizontalCenter

        WebEngineView {
            id: webView
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.verticalCenter:   parent.verticalCenter
            width  : parent.width  - 8
            height : parent.height - 8

            url: Qt.resolvedUrl("ship_viewer_json.html")

            webChannel: WebChannel {
                id: myChannel
                Component.onCompleted: {
                    myChannel.registerObject("backend", Backend)
                }
            }

            onJavaScriptConsoleMessage: {
                console.log("[JS]", message)
            }
        }

        
		
		
		Button{
		x : 400
		y : webView.height + 30
		text : "ping"
		onClicked:{
			Backend.pop("pop")
		}
		
		}
    }

    // Timer tetap tersedia jika perlu polling tambahan
    Timer {
        id: controller_gui
        interval: 100
        repeat: true
        running: true
        onTriggered: {
			//console.log(shipBackend.sensor2)
		}
    }
}
