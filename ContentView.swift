/*
iPhone側のコードです。
iPhone側のContentView.swiftにコピペしてください
*/

import SwiftUI
import HealthKit

struct ContentView: View {
    // healthKit認証関連
    @State private var labelText = "HealthKit Authorization"
    @State private var flag = false
    let healthStore = HKHealthStore()
    let allTypes = Set([HKObjectType.quantityType(forIdentifier: .heartRate)!])
    
    var body: some View {
        VStack {
            Text(labelText)
                .font(.title)
            Button(action: {
                if(self.flag) {
                    self.flag = false
                } else {
                    if HKHealthStore.isHealthDataAvailable() {
                        self.labelText = "Available"
                        self.healthStore.requestAuthorization(toShare: nil, read: self.allTypes){ (success, error) in}
                    } else {
                        self.labelText = "Unavailable"
                    }
                    self.flag = true
                }
            }){
                Text("Access")
                    .font(.largeTitle)
                    .foregroundColor(.white)
            }
            .padding(.all)
            .background(Color.blue)
            
            Spacer()
        }
        .padding()
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
