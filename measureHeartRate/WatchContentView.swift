/*
apple watch側のコードです。
watch側のContentView.swift(デフォルトだと拡張子は隠れています)にコピペしてください。
*/

import SwiftUI
import HealthKit
import Combine

struct ContentView: View {
    // healthKit認証関連
    let healthStore = HKHealthStore()
    let allTypes = Set([HKObjectType.quantityType(forIdentifier: .heartRate)!])
    let heartRateType = HKObjectType.quantityType(forIdentifier: .heartRate)!
    let heartRateUnit = HKUnit(from: "count/min")
    // workout処理関連
    @State private var workoutSessionActive = false
    @State private var hkWorkoutSession: HKWorkoutSession? = nil
    // timer処理
    @State private var timer: Timer?
    // 時間表示
    @State var nowDate = Date()
    @State var dateText = ""
    private let dateFormatter = DateFormatter()
    init() {
        dateFormatter.dateFormat = "yyyy-MM-dd'T'HH:mm:ss"
        dateFormatter.locale = Locale(identifier: "ja_jp")
    }
    // 心拍数更新処理
    @State var heartRateLatest = 0
    
    var body: some View {
        VStack {
            if workoutSessionActive {
                Button("stop workout") {
                    stopWorkoutSession()
                    timer?.invalidate()
                    workoutSessionActive = false
                }
                .padding()
            } else {
                Button("start workout") {
                    startWorkoutSession()
                    updateHeartRateNormal()
                    // 毎秒処理
                    timer = Timer.scheduledTimer(withTimeInterval: 1.0, repeats: true) { _ in
                        self.nowDate = Date()
                        dateText = "\(dateFormatter.string(from: nowDate))"
                        self.updateHeartRateNormal()
                    }
                    workoutSessionActive = true
                }
                .padding()
            }
            
            Spacer()
            
            // 時間表示
            Text(dateText)
            
            Spacer()
            
            Label(
                title: {
                    Text("心拍数")
                        .font(.title)
                },
                icon: {
                    Image(systemName: "heart.fill")
                        .font(.title)
                        .foregroundColor(.red)
                })
            
            Spacer()
            
            Text("\(String(heartRateLatest))")
                .font(.largeTitle)
            
            Spacer()
        }
        .padding()
    }
    
    // workout開始処理
    func startWorkoutSession() {
        let config = HKWorkoutConfiguration()
        config.activityType = .other
        
        do {
            let session = try HKWorkoutSession(healthStore: healthStore, configuration: config)
            session.delegate
            hkWorkoutSession = session
            session.startActivity(with: Date())
        } catch let e as NSError {
            fatalError("*** Unable to create the workout session: \(e.localizedDescription) ***")
        }
    }
    
    // workout終了処理
    func stopWorkoutSession() {
        guard let workoutSession = hkWorkoutSession else { return }
        workoutSession.stopActivity(with: Date())
    }

    // 状態変化検出時処理
    func workoutSession(_ workoutSession: HKWorkoutSession, didChangeTo toState: HKWorkoutSessionState, from fromState: HKWorkoutSessionState, date: Date) {
        switch toState {
        case .running:
            print("Workout session is running")
        case .stopped:
            print("Workout session has stopped")
            DispatchQueue.main.async() {
                self.hkWorkoutSession = nil
                // Workout終了時の追加処理を実行する場合、ここに追加
            }
        default:
            print("Unexpected workout session state: \(toState.rawValue)")
        }
    }
    
    // workoutエラー処理
    func workoutSession(_ workoutSession: HKWorkoutSession, didFailWithError error: Error) {
        NSLog("workoutSession delegate didFailWithError \(error.localizedDescription)")
    }
    
    // 心拍数更新処理
    func updateHeartRateNormal() {
        let sortDescriptors = [NSSortDescriptor(key: HKSampleSortIdentifierStartDate, ascending: false)]
        let query = HKSampleQuery(sampleType: self.heartRateType, predicate: nil, limit: 1, sortDescriptors: sortDescriptors, resultsHandler: { (query, samples, error) -> Void in
            if let error = error {
                NSLog("[updateHeartRateNormal] resultHandler error: \(error.localizedDescription)")
            } else if let samples = samples {
                let sample = samples[0] as! HKQuantitySample
                NSLog("[updateHeartRateNormal] resultHandler sample: \(sample.debugDescription)")
                let value = sample.quantity.doubleValue(for: self.heartRateUnit)
                DispatchQueue.main.async {
                    self.heartRateLatest = Int(value)
                    // debug
                    print(self.heartRateLatest)
                    
                    // データベースにデータを保存するために関数呼び出し
                    let currentTime = self.dateFormatter.string(from: self.nowDate)
                    self.saveDataToMariaDB(date: currentTime, heartRate: self.heartRateLatest)
                }
            }
        } )
        self.healthStore.execute(query)
    }
    
    // データベースにデータを保存する
    func saveDataToMariaDB (date: String, heartRate: Int) {
        guard let url = URL(string: "http://160.16.210.86:5000/api/users") else {
            print("Invalid URL")
            return
        }
        
        // リクエストのためのデータを設定
        let body: [String: Any] = [
            "time": date,
            "heartRate": heartRate
        ]
            
        // JSONエンコード
        guard let jsonData = try? JSONSerialization.data(withJSONObject: body) else {
            print("Failed to encode data")
            return
        }
        
        // リクエストの作成
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.httpBody = jsonData
            
        // URLSessionでPOSTリクエストを実行
        URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                print("Error in POST request: \(error)")
                return
            }
            
            if let httpResponse = response as? HTTPURLResponse {
                print("Server response: \(httpResponse.statusCode)")
            }
        }.resume()
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}

