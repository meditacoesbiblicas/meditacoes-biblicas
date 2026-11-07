import Vision
import CoreImage
import AppKit
let args = CommandLine.arguments
let url = URL(fileURLWithPath: args[1])
let ci = CIImage(contentsOf: url)!
let req = VNGenerateForegroundInstanceMaskRequest()
let h = VNImageRequestHandler(ciImage: ci)
try h.perform([req])
guard let obs = req.results?.first else { print("sem resultado"); exit(1) }
print("instancias:", obs.allInstances.count)
let buf = try obs.generateScaledMaskForImage(forInstances: obs.allInstances, from: h)
let mask = CIImage(cvPixelBuffer: buf)
let ctx = CIContext()
let out = ci.applyingFilter("CIBlendWithMask", parameters: [kCIInputBackgroundImageKey: CIImage.empty(), kCIInputMaskImageKey: mask])
let cg = ctx.createCGImage(out, from: ci.extent)!
let rep = NSBitmapImageRep(cgImage: cg)
try rep.representation(using: NSBitmapImageRep.FileType.png, properties: [:])!.write(to: URL(fileURLWithPath: args[2]))
let mcg = ctx.createCGImage(mask, from: ci.extent)!
try NSBitmapImageRep(cgImage: mcg).representation(using: NSBitmapImageRep.FileType.png, properties: [:])!.write(to: URL(fileURLWithPath: args[2] + ".mask.png"))
print("ok")
